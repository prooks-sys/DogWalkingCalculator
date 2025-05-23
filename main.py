def calculate_weekly_adjustment(balance):
    # Penalties for less cycles
    if balance < 0:
        if balance == -1:
            return -2.5
        elif balance == -2:
            return -5.5
        else:
            return -10
    # Bonuses for extra cycles
    elif balance > 0:
        if balance == 1:
            return 3.0
        elif balance == 2:
            return 5.0
        else:
            return 5.75
    else:
        return 0.0

def monthly_payout(total_monthly_income, weekly_balances, num_friends):
    base_weekly_pay = 20  # Updated weekly base pay
    weeks = len(weekly_balances)

    friend_totals = [0.0] * num_friends

    # Sum up all friends' pays (base + adjustments) for all weeks
    for week in weekly_balances:
        for i, balance in enumerate(week):
            adjustment = calculate_weekly_adjustment(balance)
            pay = base_weekly_pay + adjustment
            friend_totals[i] += pay

    total_friend_raw_pay = sum(friend_totals)
    if num_friends == 0:
        # No friends, boss gets all
        return [], total_monthly_income, total_monthly_income

    if total_friend_raw_pay == 0:
        # Friends earn nothing, boss gets all
        return [0.0] * num_friends, total_monthly_income, total_monthly_income

    average_friend_pay_raw = total_friend_raw_pay / num_friends
    boss_base_pay = average_friend_pay_raw * 1.5

    if boss_base_pay > total_monthly_income:
        # Income too small: boss takes all, friends get zero
        return [0.0] * num_friends, total_monthly_income, total_monthly_income

    if total_friend_raw_pay + boss_base_pay > total_monthly_income:
        # Scale down friends proportionally to fit boss base pay + friends pay in total income
        available_for_friends = total_monthly_income - boss_base_pay
        scale_factor = available_for_friends / total_friend_raw_pay
        scaled_friends = [round(pay * scale_factor, 2) for pay in friend_totals]
        boss_pay = round(boss_base_pay, 2)
        total_payout = round(sum(scaled_friends) + boss_pay, 2)
    else:
        # Pay friends full, boss gets base pay plus leftover
        scaled_friends = [round(pay, 2) for pay in friend_totals]
        leftover = total_monthly_income - (total_friend_raw_pay + boss_base_pay)
        boss_pay = round(boss_base_pay + leftover, 2)
        total_payout = total_monthly_income

    return scaled_friends, boss_pay, total_payout

def main():
    print("Dog Walking Monthly Payout Calculator\n")
    num_friends = int(input("How many friends are working? "))
    total_monthly_income = float(input("Enter total monthly income (€): "))

    weeks = 4
    weekly_balances = []

    print(f"\nEnter cycle balances per friend for each week (number of cycles extra or less, -3 to 3).")
    print(f"Use 0 if all cycles were completed.\n")

    for w in range(weeks):
        while True:
            try:
                line = input(f"Week {w+1} (space-separated {num_friends} numbers): ")
                balances = list(map(int, line.strip().split()))
                if len(balances) != num_friends:
                    print(f"Please enter exactly {num_friends} numbers.")
                    continue
                if any(b < -3 or b > 3 for b in balances):
                    print("Balances must be between -3 and 3.")
                    continue
                weekly_balances.append(balances)
                break
            except ValueError:
                print("Invalid input. Enter integers separated by spaces.")

    friends_pay, boss_pay, total_payout = monthly_payout(total_monthly_income, weekly_balances, num_friends)

    print("\n--- Monthly Payout ---")
    for i, pay in enumerate(friends_pay, 1):
        print(f"Friend {i}: €{pay}")
    print(f"Boss (You): €{boss_pay}")
    print(f"Total payout: €{total_payout}")

if __name__ == "__main__":
    main()
