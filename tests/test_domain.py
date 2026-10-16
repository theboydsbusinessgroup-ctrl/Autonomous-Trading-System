import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from ats.domain.enums import AssetClass, RiskDecisionStatus, Side
from ats.domain.models import Fill, Instrument, MarketObservation, RiskDecision, TradeIntent


NOW = datetime(2026, 10, 16, 12, tzinfo=timezone.utc)
INSTRUMENT = Instrument("SYNTHETIC", AssetClass.EQUITY)


class MarketObservationTests(unittest.TestCase):
    def test_age_and_mid_for_valid_quote(self):
        quote = MarketObservation(INSTRUMENT, NOW - timedelta(seconds=4), Decimal("100"), Decimal("102"))
        self.assertEqual(quote.age_seconds(NOW), 4)
        self.assertEqual(quote.mid, Decimal("101"))
        self.assertIsNone(MarketObservation(INSTRUMENT, NOW).mid)

    def test_future_quote_is_not_classified_as_fresh(self):
        quote = MarketObservation(INSTRUMENT, NOW + timedelta(microseconds=1))
        with self.assertRaisesRegex(ValueError, "future"):
            quote.age_seconds(NOW)

    def test_naive_timestamps_are_rejected(self):
        with self.assertRaises(ValueError):
            MarketObservation(INSTRUMENT, NOW.replace(tzinfo=None))
        with self.assertRaises(ValueError):
            MarketObservation(INSTRUMENT, NOW).age_seconds(NOW.replace(tzinfo=None))

    def test_crossed_and_invalid_prices_are_rejected(self):
        with self.assertRaises(ValueError):
            MarketObservation(INSTRUMENT, NOW, Decimal("102"), Decimal("100"))
        for price in (Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 1.0, True):
            for field in ("bid", "ask", "last"):
                with self.subTest(price=price, field=field), self.assertRaises(ValueError):
                    MarketObservation(INSTRUMENT, NOW, **{field: price})

    def test_invalid_volume_is_rejected(self):
        for volume in (-1, 1.2, True):
            with self.assertRaises(ValueError):
                MarketObservation(INSTRUMENT, NOW, volume=volume)

    def test_signed_future_prices_and_zero_option_bid_remain_representable(self):
        future = Instrument("SYNTHETIC-FUTURE", AssetClass.FUTURE)
        quote = MarketObservation(future, NOW, Decimal("-2"), Decimal("-1"))
        self.assertEqual(quote.mid, Decimal("-1.5"))
        TradeIntent(future, Side.BUY, Decimal("1"), "synthetic", .5, NOW, limit_price=Decimal("-1"))
        option = Instrument("SYNTHETIC-OPTION", AssetClass.OPTION)
        MarketObservation(option, NOW, Decimal("0"), Decimal(".01"))
        self.assertEqual(Fill("test", NOW, Decimal("1"), Decimal("-1")).price, Decimal("-1"))


class TradingContractTests(unittest.TestCase):
    def intent(self, quantity=Decimal("1"), **kwargs):
        return TradeIntent(INSTRUMENT, Side.BUY, quantity, "synthetic", 0.5, NOW, **kwargs)

    def test_valid_intent_preserves_decimal_quantity(self):
        self.assertEqual(self.intent(Decimal("1.25")).quantity, Decimal("1.25"))

    def test_nonpositive_and_nonfinite_intent_quantities_are_rejected(self):
        for quantity in (Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 1.0):
            with self.assertRaises(ValueError):
                self.intent(quantity)

    def test_invalid_intent_prices_are_rejected(self):
        for field in ("limit_price", "stop_price"):
            with self.assertRaises(ValueError):
                self.intent(**{field: Decimal("0")})

    def test_rejected_risk_decision_cannot_approve_quantity(self):
        with self.assertRaises(ValueError):
            RiskDecision(RiskDecisionStatus.REJECTED, "blocked", Decimal("1"))
        self.assertEqual(RiskDecision(RiskDecisionStatus.REJECTED, "blocked").approved_quantity, Decimal("0"))

    def test_approval_requires_positive_finite_quantity(self):
        for status in (RiskDecisionStatus.APPROVED, RiskDecisionStatus.REDUCED):
            for quantity in (Decimal("0"), Decimal("-1"), Decimal("NaN")):
                with self.assertRaises(ValueError):
                    RiskDecision(status, "synthetic", quantity)
            self.assertEqual(RiskDecision(status, "synthetic", Decimal("1")).approved_quantity, Decimal("1"))

    def test_invalid_fill_values_are_rejected(self):
        for values in ({"quantity": Decimal("-1")}, {"price": Decimal("NaN")}, {"fee": Decimal("Infinity")}):
            data = dict(order_id="test", timestamp=NOW, quantity=Decimal("1"), price=Decimal("100"))
            data.update(values)
            with self.assertRaises(ValueError):
                Fill(**data)
        self.assertEqual(Fill("test", NOW, Decimal("1"), Decimal("100"), Decimal("-0.01")).fee, Decimal("-0.01"))


if __name__ == "__main__":
    unittest.main()
