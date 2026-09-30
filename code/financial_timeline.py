from datetime import datetime, timedelta


class FinancialTimeline:
    FORECAST_DAYS = 90

    def __init__(
    self,
    exchange_rates=None,
    currency_converter=None,
    messages=None,
    images=None
   ):
        self.exchange_rates = exchange_rates or {}
        self.currency_converter = currency_converter
        self.messages = messages if messages is not None else []
        self.images = images if images is not None else []

    def build(
        self,
        starting_balance,
        start_date,
        events,
        home_currency=None
    ):
        start = self._date(start_date)

        if start is None:
            return []

        end = start + timedelta(days=self.FORECAST_DAYS)

        result = []
        balance = float(starting_balance)

        prepared = []

        for event in events:

            status = str(
                event.get("status", "")
            ).lower().strip()

            if status in ("failed", "cancelled"):
                continue

            event_date = self._effective_date(event)

            if event_date is None:
                continue

            if event_date < start or event_date > end:
                continue

            amount = self._number(
                event.get("amount")
            )

            if amount is None:
                continue

            amount = self.convert_amount(
                amount,
                event.get("currency"),
                home_currency,
                event_date
            )

            item = dict(event)
            item["amount"] = amount
            item["_effective_date"] = event_date

            prepared.append(item)

        prepared.sort(
            key=lambda x: x["_effective_date"]
        )

        for event in prepared:

            direction = str(
                event.get("direction", "")
            ).lower().strip()

            if direction == "credit":
                balance += float(event["amount"])

            elif direction == "debit":
                balance -= float(event["amount"])

            event["balance_after"] = balance

            result.append(event)

        return result

    def is_minimum_balance_safe(
        self,
        starting_balance,
        start_date,
        events,
        minimum_balance,
        home_currency=None
    ):
        timeline = self.build(
            starting_balance,
            start_date,
            events,
            home_currency
        )

        balance = float(starting_balance)
        minimum_balance = float(minimum_balance)

        for event in timeline:

            direction = str(
                event.get("direction", "")
            ).lower().strip()

            amount = float(event["amount"])

            if direction == "credit":
                balance += amount

            elif direction == "debit":
                balance -= amount

            if balance < minimum_balance:
                return False

        return True
    # ---------------------------------------------------------
    # BASIC HELPERS
    # ---------------------------------------------------------

    def _date(self, value):
        if value is None:
            return None

        text = str(value)

        if text in ("", "nan", "NaT", "None"):
            return None

        return datetime.strptime(text[:10], "%Y-%m-%d").date()

    def _date_range(self, start_date, days=None):
        start = self._date(start_date)

        if start is None:
            return []

        days = self.FORECAST_DAYS if days is None else days

        return [
            start + timedelta(days=i)
            for i in range(days + 1)
        ]

    def _number(self, value):
        try:
            if value is None:
                return None

            text = str(value).strip()

            if text in ("", "nan", "NaN", "None"):
                return None

            return float(text)

        except (TypeError, ValueError):
            return None

    # ---------------------------------------------------------
    # CURRENCY
    # ---------------------------------------------------------

    def convert_amount(self, amount, from_currency, to_currency, date):
        amount = self._number(amount)

        if amount is None:
            return None

        if not from_currency or not to_currency:
            return amount

        if str(from_currency) == str(to_currency):
            return amount

        key = (
            str(date),
            str(from_currency),
            str(to_currency)
        )

        if self.currency_converter is not None:
            return self.currency_converter.convert(
                amount,
                from_currency,
                to_currency,
                str(date)
            )

        if key in self.exchange_rates:
            return amount * float(self.exchange_rates[key])

        reverse_key = (
            str(date),
            str(to_currency),
            str(from_currency)
        )

        if reverse_key in self.exchange_rates:
            rate = float(self.exchange_rates[reverse_key])

            if rate != 0:
                return amount / rate

        return amount

    # ---------------------------------------------------------
    # EVENT DATE
    # ---------------------------------------------------------

    def _effective_date(self, event):
        settlement = self._date(event.get("settlement_date"))

        if settlement is not None:
            return settlement

        return self._date(event.get("event_date"))

    # ---------------------------------------------------------
    # EVENT VALIDITY
    # ---------------------------------------------------------

    def _valid_event(self, event):
        status = str(event.get("status", "")).lower().strip()

        if status in ("failed", "cancelled"):
            return False

        direction = str(
            event.get("direction", "")
        ).lower().strip()

        # Pending credits are not confirmed income.
        if status == "pending" and direction == "credit":
            return False

        # Ignore unknown statuses.
        if status not in (
            "settled",
            "confirmed",
            "scheduled",
            "pending"
        ):
            return False

        return True

    # ---------------------------------------------------------
    # EVENT AMOUNT
    # ---------------------------------------------------------

    def _event_amount(
        self,
        event,
        home_currency=None,
        date=None
    ):
        amount = self._number(event.get("amount"))

        if amount is None:
            return None

        currency = event.get("currency")

        return self.convert_amount(
            amount,
            currency,
            home_currency,
            date or self._effective_date(event)
        )
    # ---------------------------------------------------------
    # PREPARE EVENTS
    # ---------------------------------------------------------

    def prepare_events(
        self,
        events,
        request_date,
        home_currency=None
    ):
        start = self._date(request_date)

        if start is None:
            return []

        end = start + timedelta(days=self.FORECAST_DAYS)

        valid = []

        for event in events:

            if not self._valid_event(event):
                continue

            effective_date = self._effective_date(event)

            if effective_date is None:
                continue

            amount = self._event_amount(
                event,
                home_currency,
                effective_date
            )

            if amount is None:
                continue

            copy = dict(event)
            copy["_effective_date"] = effective_date
            copy["_amount"] = amount

            valid.append(copy)

        # -----------------------------------------------------
        # Historical recurring events
        # -----------------------------------------------------

        series = {}

        for event in valid:

            date = event["_effective_date"]

            if date >= start:
                continue

            key = (
                str(event.get("event_type", "")),
                str(event.get("description", "")),
                str(event.get("category", "")),
                str(event.get("direction", "")),
                str(event.get("currency", ""))
            )

            series.setdefault(key, []).append(event)

        projected = []

        for key, history in series.items():

            history.sort(
                key=lambda x: x["_effective_date"]
            )

            if len(history) < 2:
                continue

            recent = history[-6:]

            intervals = []

            for i in range(1, len(recent)):

                diff = (
                    recent[i]["_effective_date"]
                    - recent[i - 1]["_effective_date"]
                ).days

                if diff > 0:
                    intervals.append(diff)

            if not intervals:
                continue

            median_interval = sorted(intervals)[
                len(intervals) // 2
            ]

            if median_interval < 5 or median_interval > 45:
                continue

            if any(
                abs(x - median_interval)
                > max(4, median_interval * 0.25)
                for x in intervals
            ):
                continue

            template = history[-1]

            next_date = (
                template["_effective_date"]
                + timedelta(days=median_interval)
            )

            while next_date <= end:

                if next_date >= start:

                    projected_event = dict(template)

                    projected_event["_effective_date"] = next_date
                    projected_event["_amount"] = template["_amount"]

                    projected_event["event_id"] = template.get(
                        "event_id"
                    )

                    projected_event["settlement_date"] = (
                        next_date.isoformat()
                    )

                    projected_event["event_date"] = (
                        next_date.isoformat()
                    )

                    projected_event["_projected_recurring"] = True

                    projected.append(projected_event)

                next_date += timedelta(
                    days=median_interval
                )

        # -----------------------------------------------------
        # Explicit future events take priority.
        # Do not create projected copies when an actual event
        # already exists for the same recurring series/date.
        # -----------------------------------------------------

        actual_keys = set()

        for event in valid:

            date = event["_effective_date"]

            if start <= date <= end:

                key = (
                    str(event.get("event_type", "")),
                    str(event.get("description", "")),
                    str(event.get("category", "")),
                    str(event.get("direction", "")),
                    str(event.get("currency", "")),
                    date
                )

                actual_keys.add(key)

        all_events = []

        for event in valid:

            date = event["_effective_date"]

            if start <= date <= end:
                all_events.append(event)

        for event in projected:

            date = event["_effective_date"]

            key = (
                str(event.get("event_type", "")),
                str(event.get("description", "")),
                str(event.get("category", "")),
                str(event.get("direction", "")),
                str(event.get("currency", "")),
                date
            )

            if key in actual_keys:
                continue

            all_events.append(event)

        # -----------------------------------------------------
        # Deduplicate
        # -----------------------------------------------------

        result = []
        seen = set()

        for event in all_events:

            fingerprint = (
                str(event.get("event_id", "")),
                event["_effective_date"],
                str(event.get("direction", "")),
                round(float(event["_amount"]), 8)
            )

            if fingerprint in seen:
                continue

            seen.add(fingerprint)
            result.append(event)

        result.sort(
            key=lambda x: (
                x["_effective_date"],
                str(x.get("event_id", ""))
            )
        )

        return result
    # ---------------------------------------------------------
    # BALANCE TIMELINE
    # ---------------------------------------------------------

    def _daily_balances(
       self,
       starting_balance,
       start_date,
       events,
       home_currency=None
    ):
        starting_balance = float(starting_balance)

        # Events may already be prepared/projected.
        # Do not prepare them a second time.
        if events and all(
            "_effective_date" in event and "_amount" in event
            for event in events
        ):
            prepared = events
        else:
            prepared = self.prepare_events(
                events,
                start_date,
                home_currency
            )

        by_date = {}

        for event in prepared:
            date = event["_effective_date"]

            by_date.setdefault(date, []).append(event)

        balances = {}

        balance = starting_balance

        for date in self._date_range(
            start_date,
            self.FORECAST_DAYS
        ):
            for event in by_date.get(date, []):

                amount = event["_amount"]

                if event.get("direction") == "credit":
                    balance += amount

                elif event.get("direction") == "debit":
                    balance -= amount

            balances[date.isoformat()] = balance

        return balances
    # ---------------------------------------------------------
    # APPLY SPENDING CHANGES
    # ---------------------------------------------------------

    def _modified_events(
        self,
        events,
        changes
    ):
        if not changes:
            return events

        result = []

        stop_ids = set()
        reduce_values = {}

        for change in changes:

            if change.startswith("stop:"):
                stop_ids.add(
                    change.split(":", 1)[1]
                )

            elif change.startswith("reduce_to:"):

                parts = change.split(":")

                if len(parts) == 3:
                    try:
                        reduce_values[
                            parts[1]
                        ] = float(parts[2])
                    except ValueError:
                        pass

        for event in events:

            event_copy = dict(event)

            event_id = str(
                event.get("event_id", "")
            )

            if event_id in stop_ids:
                continue

            if event_id in reduce_values:

                current_amount = event_copy.get(
                    "_amount"
                )

                if current_amount is not None:
                    minimum = reduce_values[event_id]

                    event_copy["_amount"] = min(
                        float(current_amount),
                        minimum
                    )

            result.append(event_copy)

        return result

    # ---------------------------------------------------------
    # SAFETY CHECK
    # ---------------------------------------------------------

    def is_payment_schedule_safe(
        self,
        starting_balance,
        start_date,
        events,
        payments,
        minimum_balance,
        home_currency=None
    ):
        balances = self._daily_balances(
            starting_balance,
            start_date,
            events,
            home_currency
        )

        payment_by_date = {}

        for payment in payments:

            date = str(payment["date"])

            amount = float(
                payment["amount"]
            )

            payment_by_date[date] = (
                payment_by_date.get(date, 0.0)
                + amount
            )

        running_payments = 0.0

        for date, balance in balances.items():

            if date in payment_by_date:
                running_payments += (
                    payment_by_date[date]
                )

            effective_balance = (
                balance - running_payments
            )

            if effective_balance < float(
                minimum_balance
            ):
                return False

        return True

    # ---------------------------------------------------------
    # SAFE AMOUNT TODAY
    # ---------------------------------------------------------

    def get_safe_amount_today(
        self,
        starting_balance,
        start_date,
        events,
        minimum_balance,
        requested_amount,
        home_currency=None
    ):
        balances = self._daily_balances(
            starting_balance,
            start_date,
            events,
            home_currency
        )

        if not balances:
            return 0.0

        minimum_forecast_balance = min(
            balances.values()
        )

        safe_amount = (
            minimum_forecast_balance
            - float(minimum_balance)
        )

        safe_amount = max(
            0.0,
            safe_amount
        )

        return min(
            safe_amount,
            float(requested_amount)
        )

    # ---------------------------------------------------------
    # EARLIEST FULL PAYMENT DATE
    # ---------------------------------------------------------

    def find_earliest_full_payment_date(
        self,
        starting_balance,
        request_date,
        desired_date,
        requested_amount,
        events,
        minimum_balance,
        home_currency=None
    ):
        request_day = self._date(request_date)
        desired_day = self._date(desired_date)

        if request_day is None or desired_day is None:
            return None

        balances = self._daily_balances(
            starting_balance,
            request_date,
            events,
            home_currency
        )

        for date in self._date_range(
            request_date,
            self.FORECAST_DAYS
        ):

            if date > desired_day:
                break

            date_string = date.isoformat()

            if date_string not in balances:
                continue

            payments = [
                {
                    "date": date_string,
                    "amount": requested_amount
                }
            ]

            if self.is_payment_schedule_safe(
                starting_balance,
                request_date,
                events,
                payments,
                minimum_balance,
                home_currency
            ):
                return date_string

        return None

    # ---------------------------------------------------------
    # PAYMENT OPTIONS
    # ---------------------------------------------------------

    def get_payment_options_for_request(
        self,
        payment_options,
        request_id
    ):
        return [
            option
            for option in payment_options
            if str(option.get("request_id"))
            == str(request_id)
        ]

    def _option_payment_dates(self, option):

        first_date = self._date(
            option.get("first_payment_date")
        )

        number_of_payments = self._number(
            option.get("number_of_payments")
        )

        frequency_days = self._number(
            option.get("payment_frequency_days")
        )

        if (
            first_date is None
            or number_of_payments is None
            or frequency_days is None
        ):
            return None

        number_of_payments = int(
            number_of_payments
        )

        frequency_days = int(
            frequency_days
        )

        if number_of_payments <= 0:
            return None

        dates = []

        for i in range(number_of_payments):

            date = first_date + timedelta(
                days=i * frequency_days
            )

            dates.append(
                date.isoformat()
            )

        return dates

    def build_payment_plan(
        self,
        payment_option,
        requested_amount=None
    ):
        dates = self._option_payment_dates(
            payment_option
        )

        if not dates:
            return None

        payment_amount = self._number(
            payment_option.get("payment_amount")
        )

        if payment_amount is None:
            return None

        return [
            {
                "date": date,
                "amount": round(
                    payment_amount,
                    2
                )
            }
            for date in dates
        ]

    def select_payment_option(
        self,
        payment_options,
        request_id,
        requested_amount,
        request_date,
        desired_date,
        starting_balance,
        events,
        minimum_balance,
        accepted_methods,
        home_currency=None,
        max_installment_months=None
    ):
        if "installments" not in accepted_methods:
            return None

        options = self.get_payment_options_for_request(
            payment_options,
            request_id
        )

        request_day = self._date(request_date)
        desired_day = self._date(desired_date)

        valid_options = []

        for option in options:

            plan = self.build_payment_plan(
                option,
                requested_amount
            )

            if not plan:
                continue

            first_day = self._date(
                plan[0]["date"]
            )

            last_day = self._date(
                plan[-1]["date"]
            )

            if first_day < request_day:
                continue

            if last_day > desired_day:
                continue

            # Respect profile's maximum installment period.
            if max_installment_months is not None:

                months = self._number(
                    max_installment_months
                )

                if months is not None:

                    max_days = int(
                        months * 31
                    )

                    if (
                        last_day - request_day
                    ).days > max_days:
                        continue

            if not self.is_payment_schedule_safe(
                starting_balance,
                request_date,
                events,
                plan,
                minimum_balance,
                home_currency
            ):
                continue

            total = self._number(
                option.get(
                    "total_payable_amount"
                )
            )

            if total is None:
                continue

            number_of_payments = int(
                self._number(
                    option.get(
                        "number_of_payments"
                    )
                ) or len(plan)
            )

            valid_options.append(
                {
                    "option": option,
                    "plan": plan,
                    "total": total,
                    "first_date": first_day,
                    "number_of_payments":
                        number_of_payments
                }
            )

        if not valid_options:
            return None

        valid_options.sort(
            key=lambda x: (
                x["total"],
                x["first_date"],
                x["number_of_payments"],
                str(
                    x["option"].get(
                        "payment_option_id",
                        ""
                    )
                )
            )
        )

        return valid_options[0]

    # ---------------------------------------------------------
    # PARTIAL PAYMENT
    # ---------------------------------------------------------

    def build_partial_payment_plan(
        self,
        requested_amount,
        safe_amount,
        request_date,
        full_payment_date
    ):
        if (
            safe_amount <= 0
            or safe_amount >= requested_amount
            or not full_payment_date
        ):
            return None

        remaining = (
            float(requested_amount)
            - float(safe_amount)
        )

        return [
            {
                "date": str(request_date),
                "amount": round(
                    float(safe_amount),
                    2
                )
            },
            {
                "date": str(full_payment_date),
                "amount": round(
                    remaining,
                    2
                )
            }
        ]

    # ---------------------------------------------------------
    # SPENDING CHANGES
    # ---------------------------------------------------------

    def _candidate_spending_changes(
        self,
        events,
        allowed_reduce_categories,
        allowed_stop_categories
    ):
        candidates = []

        for event in events:

            if str(
                event.get("flexibility", "")
            ).lower() != "flexible":
                continue

            event_id = str(
                event.get("event_id", "")
            )

            category = str(
                event.get("category", "")
            )

            amount = event.get("_amount")

            if amount is None:
                continue

            # Stopping is preferred only when explicitly allowed.
            if category in allowed_stop_categories:
                candidates.append(
                    (
                        0,
                        event_id,
                        f"stop:{event_id}"
                    )
                )

            # Reduction is also considered.
            if category in allowed_reduce_categories:

                minimum = self._number(
                    event.get(
                        "minimum_allowed_amount"
                    )
                )

                if minimum is not None:
                    candidates.append(
                        (
                            1,
                            event_id,
                            f"reduce_to:{event_id}:{minimum:g}"
                        )
                    )

        unique = {}
        for priority, event_id, change in candidates:
            # Stop/reduce for the same event are mutually exclusive.
            # Keep the preferred representation only.
            if event_id not in unique or priority < unique[event_id][0]:
                unique[event_id] = (priority, event_id, change)

        return list(unique.values())

    def find_spending_change_plan(
        self,
        events,
        allowed_reduce_categories,
        allowed_stop_categories,
        payment_checker
    ):
        candidates = self._candidate_spending_changes(
            events,
            allowed_reduce_categories,
            allowed_stop_categories
        )

        # No change first.
        if payment_checker(events, []):
            return []

        # One change.
        for _, _, change in candidates:

            if payment_checker(
                events,
                [change]
            ):
                return [change]

        # Two changes.
        for i in range(len(candidates)):

            for j in range(i + 1, len(candidates)):

                changes = [
                    candidates[i][2],
                    candidates[j][2]
                ]

                if payment_checker(
                    events,
                    changes
                ):
                    return changes

        # Three changes.
        for i in range(len(candidates)):

            for j in range(i + 1, len(candidates)):

                for k in range(j + 1, len(candidates)):

                    changes = [
                        candidates[i][2],
                        candidates[j][2],
                        candidates[k][2]
                    ]

                    if payment_checker(
                        events,
                        changes
                    ):
                        return changes

        return None

    # ---------------------------------------------------------
    # FORMAT
    # ---------------------------------------------------------

    def format_payment_plan(self, payments):

        if not payments:
            return "none"

        return "|".join(
            f"{p['date']}:{p['amount']:.2f}"
            for p in payments
        )

    def format_spending_changes(self, changes):

        if not changes:
            return "none"

        return "|".join(
            changes[:3]
        )

    # ---------------------------------------------------------
    # REQUEST PROCESSING
    # ---------------------------------------------------------

    def process_request(
        self,
        request,
        profile,
        events,
        payment_options
    ):
        payroll_updates = self.extract_confirmed_payroll_updates(
            user_id=request.get("user_id"),
            request_id=request.get("request_id")
        )
        requested_amount = float(
            request["requested_amount"]
        )

        request_date = str(
            request["request_date"]
        )

        desired_date = str(
            request["desired_completion_date"]
        )

        starting_balance = float(
            profile["current_available_balance"]
        )

        minimum_balance = float(
            profile["minimum_balance_to_keep"]
        )

        home_currency = profile.get(
            "home_currency"
        )

        accepted_methods = [
            x.strip()
            for x in str(
                profile.get(
                    "payment_methods_user_will_consider",
                    ""
                )
            ).split("|")
            if x.strip()
        ]

        allowed_reduce_categories = set(
            x.strip()
            for x in str(
                profile.get(
                    "expense_categories_user_is_willing_to_reduce",
                    ""
                )
            ).split("|")
            if x.strip()
        )

        allowed_stop_categories = set(
            x.strip()
            for x in str(
                profile.get(
                    "expense_categories_user_is_willing_to_stop",
                    ""
                )
            ).split("|")
            if x.strip()
        )

        max_installment_months = (
            profile.get(
                "max_installment_months"
            )
        )

        prepared_events = self.prepare_events(
            events,
            request_date,
            home_currency
        )

        # Apply confirmed payroll information only.
        # Pending/unapproved payroll messages are ignored.
        if payroll_updates:
            for update in payroll_updates:
                request["_payroll_evidence"] = update
        # -----------------------------------------------------
        # SAFE AMOUNT BEFORE OPTIONAL CHANGES
        # -----------------------------------------------------

        amount_safe_to_pay = self.get_safe_amount_today(
            starting_balance,
            request_date,
            prepared_events,
            minimum_balance,
            requested_amount,
            home_currency
        )

        amount_safe_to_pay = round(
            amount_safe_to_pay,
            2
        )

        # -----------------------------------------------------
        # EARLIEST DATE WITHOUT CHANGES
        # -----------------------------------------------------

        earliest_full_payment_date = (
            self.find_earliest_full_payment_date(
                starting_balance,
                request_date,
                desired_date,
                requested_amount,
                prepared_events,
                minimum_balance,
                home_currency
            )
        )

        # -----------------------------------------------------
        # IMMEDIATE FULL PAYMENT WITHOUT CHANGES
        # -----------------------------------------------------

        immediate_plan = [
            {
                "date": request_date,
                "amount": requested_amount
            }
        ]

        immediate_safe = self.is_payment_schedule_safe(
            starting_balance,
            request_date,
            prepared_events,
            immediate_plan,
            minimum_balance,
            home_currency
        )

        # -----------------------------------------------------
        # OPTIONAL SPENDING CHANGES
        # -----------------------------------------------------

        def check_full_payment(event_list, changes):
            modified = self._modified_events(
                event_list,
                changes
            )

            return self.is_payment_schedule_safe(
                starting_balance,
                request_date,
                modified,
                immediate_plan,
                minimum_balance,
                home_currency
            )

        spending_changes = []

        if not immediate_safe:

            changes = self.find_spending_change_plan(
                prepared_events,
                allowed_reduce_categories,
                allowed_stop_categories,
                check_full_payment
            )

            if changes is not None:
                spending_changes = changes

        # -----------------------------------------------------
        # FULL PAYMENT NOW
        # -----------------------------------------------------

        if immediate_safe and "full_payment" in accepted_methods:

            return {
                "request_id":
                    request["request_id"],
                "amount_safe_to_pay":
                    amount_safe_to_pay,
                "affordability_status":
                    "affordable_now",
                "recommended_payment_method":
                    "full_payment",
                "payment_plan":
                    self.format_payment_plan(
                        immediate_plan
                    ),
                "earliest_date_for_full_payment":
                    request_date,
                "spending_changes_needed":
                    "none",
                "decision_explanation":
                    "The requested amount is safe "
                    "to pay immediately while "
                    "maintaining the required "
                    "minimum balance."
            }

        # -----------------------------------------------------
        # FULL PAYMENT NOW WITH SPENDING CHANGES
        # -----------------------------------------------------

        if (
            spending_changes
            and "full_payment" in accepted_methods
            and check_full_payment(
                prepared_events,
                spending_changes
            )
        ):

            return {
                "request_id":
                    request["request_id"],
                "amount_safe_to_pay":
                    amount_safe_to_pay,
                "affordability_status":
                    "affordable_with_plan",
                "recommended_payment_method":
                    "full_payment",
                "payment_plan":
                    self.format_payment_plan(
                        immediate_plan
                    ),
                "earliest_date_for_full_payment":
                    request_date,
                "spending_changes_needed":
                    self.format_spending_changes(
                        spending_changes
                    ),
                "decision_explanation":
                    "The requested amount can be "
                    "paid on the request date after "
                    "the permitted flexible spending "
                    "changes are applied."
            }

        # -----------------------------------------------------
        # INSTALLMENTS WITHOUT CHANGES
        # -----------------------------------------------------

        selected_option = self.select_payment_option(
            payment_options,
            request["request_id"],
            requested_amount,
            request_date,
            desired_date,
            starting_balance,
            prepared_events,
            minimum_balance,
            accepted_methods,
            home_currency,
            max_installment_months
        )

        if selected_option is not None:

            return {
                "request_id":
                    request["request_id"],
                "amount_safe_to_pay":
                    amount_safe_to_pay,
                "affordability_status":
                    "affordable_with_plan",
                "recommended_payment_method":
                    "installments",
                "payment_plan":
                    self.format_payment_plan(
                        selected_option["plan"]
                    ),
                "earliest_date_for_full_payment":
                    earliest_full_payment_date,
                "spending_changes_needed":
                    "none",
                "decision_explanation":
                    "The requested amount can be "
                    "completed safely using the "
                    "eligible installment option."
            }

        # -----------------------------------------------------
        # PARTIAL PAYMENT
        # -----------------------------------------------------

        allows_partial = str(
            request.get(
                "allows_partial_payment",
                ""
            )
        ).lower() in (
            "true",
            "1",
            "yes"
        )

        if (
            allows_partial
            and "partial_payment" in accepted_methods
            and amount_safe_to_pay > 0
            and amount_safe_to_pay < requested_amount
            and earliest_full_payment_date is not None
        ):

            partial_plan = (
                self.build_partial_payment_plan(
                    requested_amount,
                    amount_safe_to_pay,
                    request_date,
                    earliest_full_payment_date
                )
            )

            if partial_plan:

                if self.is_payment_schedule_safe(
                    starting_balance,
                    request_date,
                    prepared_events,
                    partial_plan,
                    minimum_balance,
                    home_currency
                ):

                    return {
                        "request_id":
                            request["request_id"],
                        "amount_safe_to_pay":
                            amount_safe_to_pay,
                        "affordability_status":
                            "affordable_with_plan",
                        "recommended_payment_method":
                            "partial_payment",
                        "payment_plan":
                            self.format_payment_plan(
                                partial_plan
                            ),
                        "earliest_date_for_full_payment":
                            earliest_full_payment_date,
                        "spending_changes_needed":
                            "none",
                        "decision_explanation":
                            "A partial payment can be "
                            "made immediately and the "
                            "remaining amount can be "
                            "paid when the full request "
                            "becomes safe."
                    }

        # -----------------------------------------------------
        # WAIT
        # -----------------------------------------------------

        if (
            earliest_full_payment_date is not None
            and "full_payment" in accepted_methods
        ):

            return {
                "request_id":
                    request["request_id"],
                "amount_safe_to_pay":
                    amount_safe_to_pay,
                "affordability_status":
                    "affordable_later",
                "recommended_payment_method":
                    "wait",
                "payment_plan":
                    self.format_payment_plan(
                        [
                            {
                                "date":
                                    earliest_full_payment_date,
                                "amount":
                                    requested_amount
                            }
                        ]
                    ),
                "earliest_date_for_full_payment":
                    earliest_full_payment_date,
                "spending_changes_needed":
                    "none",
                "decision_explanation":
                    "The requested amount is not safe "
                    "today but becomes safe later "
                    "within the requested deadline."
            }

        # -----------------------------------------------------
        # NOT AFFORDABLE
        # -----------------------------------------------------

        return {
            "request_id":
                request["request_id"],
            "amount_safe_to_pay":
                amount_safe_to_pay,
            "affordability_status":
                "not_affordable",
            "recommended_payment_method":
                "not_recommended",
            "payment_plan":
                "none",
            "earliest_date_for_full_payment":
                earliest_full_payment_date,
            "spending_changes_needed":
                "none",
            "decision_explanation":
                "The requested amount cannot be "
                "completed safely within the available "
                "forecast and payment constraints."
        }


        # ---------------------------------------------------------
    # MESSAGE / IMAGE EVIDENCE
    # ---------------------------------------------------------

    def get_user_messages(self, user_id, request_id=None):
        """
        Return messages relevant to the current user/request.
        """

        if self.messages is None:
            return []

        if hasattr(self.messages, "to_dict"):
            records = self.messages.to_dict("records")
        elif isinstance(self.messages, dict):
            records = list(self.messages.values())
        else:
            records = list(self.messages)

        results = []

        for message in records:

            if not isinstance(message, dict):
                continue

            if str(message.get("user_id")) != str(user_id):
                continue

            message_request_id = message.get("request_id")

            if request_id is not None:
                if (
                    message_request_id is not None
                    and str(message_request_id)
                    != str(request_id)
                ):
                    continue

            results.append(message)

        return results


    def get_request_images(self, user_id, request_id=None):
        """
        Return image metadata linked to the current user/request.
        """

        if self.images is None:
            return []

        if hasattr(self.images, "to_dict"):
            records = self.images.to_dict("records")
        elif isinstance(self.images, dict):
            records = list(self.images.values())
        else:
            records = list(self.images)

        results = []

        for image in records:

            if not isinstance(image, dict):
                continue

            if str(image.get("user_id")) != str(user_id):
                continue

            image_request_id = image.get("request_id")

            if request_id is not None:
                if (
                    image_request_id is not None
                    and str(image_request_id)
                    != str(request_id)
                ):
                    continue

            results.append(image)

        return results


    def extract_confirmed_payroll_updates(
        self,
        user_id,
        request_id=None
    ):
        """
        Extract simple confirmed payroll information from
        employer messages.

        Only explicit/confirmed information is considered.
        Pending or unapproved amounts are ignored.
        """

        messages = self.get_user_messages(
            user_id,
            request_id
        )

        updates = []

        salary_words = [
            "salary",
            "payroll",
            "monthly pay",
            "monthly salary",
            "gaji",
            "penggajian",
            "pay"
        ]

        uncertain_words = [
            "pending",
            "not approved",
            "not confirmed",
            "belum disetujui",
            "menunggu",
            "waiting",
            "uncertain"
        ]

        confirmed_words = [
            "confirmed",
            "scheduled",
            "expected",
            "updated",
            "changes",
            "changed",
            "naik",
            "rutin",
            "dikonfirmasi"
        ]

        for message in messages:

            text = str(
                message.get(
                    "message_text",
                    ""
                )
            ).strip()

            if not text:
                continue

            lower_text = text.lower()

            if not any(
                word in lower_text
                for word in salary_words
            ):
                continue

            if any(
                word in lower_text
                for word in uncertain_words
            ):
                continue

            if not any(
                word in lower_text
                for word in confirmed_words
            ):
                continue

            updates.append(
                {
                    "message_id": message.get(
                        "message_id"
                    ),
                    "sent_at": message.get(
                        "sent_at"
                    ),
                    "source_type": message.get(
                        "source_type"
                    ),
                    "message_text": text
                }
            )

        return updates
