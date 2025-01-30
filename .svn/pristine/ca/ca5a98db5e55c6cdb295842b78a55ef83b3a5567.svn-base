from Helper_Files.send_error_log import send_error_log
# def calculate_sma(data, period):
#     close_prices = data["close"]
#     sma = []

#     if period is None:
#         return None

#     for i in range(len(close_prices)):
#         if i < period - 1:
#             sma.append(None)
#         else:
#             sma.append(sum(close_prices[i - period + 1:i + 1]) / period)

#     return sma[-1] if sma else None


from Helper_Files.send_error_log import send_error_log

def calculate_sma(data, period):
    try:
        close_prices = data["close"]
        sma = []

        if period is None:
            return None

        for i in range(len(close_prices)):
            if i < period - 1:
                sma.append(None)
            else:
                sma.append(sum(close_prices[i - period + 1:i + 1]) / period)

        return sma[-1] if sma else None
    except Exception as e:
        error_message = f"Error calculating SMA: {str(e)}"
        send_error_log(error_message, 'calculate_sma')
        return None
