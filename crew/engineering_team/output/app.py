import gradio as gr
from accounts import Account

# Create a single account instance for demonstration
account = Account(account_id="user123", initial_deposit=1000.0)

def deposit_funds(amount):
    try:
        account.deposit(amount)
        return f"Deposited {amount}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def withdraw_funds(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew {amount}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def buy_share(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} of {symbol}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def sell_share(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} of {symbol}. New balance: {account.balance}"
    except ValueError as e:
        return str(e)

def get_portfolio_value():
    return f"Total portfolio value: {account.get_portfolio_value()}"

def get_profit_loss():
    return f"Profit/Loss: {account.get_profit_loss()}"

def get_holdings():
    return str(account.get_holdings())

def get_transactions():
    return str(account.get_transactions())

with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Account Management")
    
    with gr.Tab("Deposit/Withdraw"):
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit")
        deposit_result = gr.Textbox(label="Deposit Result", interactive=False)
        deposit_button.click(deposit_funds, inputs=deposit_amount, outputs=deposit_result)

        withdraw_amount = gr.Number(label="Withdraw Amount")
        withdraw_button = gr.Button("Withdraw")
        withdraw_result = gr.Textbox(label="Withdraw Result", interactive=False)
        withdraw_button.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_result)

    with gr.Tab("Buy/Sell Shares"):
        share_symbol = gr.Textbox(label="Share Symbol (e.g., AAPL)")
        buy_quantity = gr.Number(label="Buy Quantity")
        buy_button = gr.Button("Buy Shares")
        buy_result = gr.Textbox(label="Buy Result", interactive=False)
        buy_button.click(buy_share, inputs=[share_symbol, buy_quantity], outputs=buy_result)

        sell_quantity = gr.Number(label="Sell Quantity")
        sell_button = gr.Button("Sell Shares")
        sell_result = gr.Textbox(label="Sell Result", interactive=False)
        sell_button.click(sell_share, inputs=[share_symbol, sell_quantity], outputs=sell_result)

    with gr.Tab("Portfolio and Transactions"):
        portfolio_value_button = gr.Button("Get Portfolio Value")
        portfolio_value_result = gr.Textbox(label="Portfolio Value", interactive=False)
        portfolio_value_button.click(get_portfolio_value, outputs=portfolio_value_result)

        profit_loss_button = gr.Button("Get Profit/Loss")
        profit_loss_result = gr.Textbox(label="Profit/Loss", interactive=False)
        profit_loss_button.click(get_profit_loss, outputs=profit_loss_result)

        holdings_button = gr.Button("Get Holdings")
        holdings_result = gr.Textbox(label="Holdings", interactive=False)
        holdings_button.click(get_holdings, outputs=holdings_result)

        transactions_button = gr.Button("Get Transactions")
        transactions_result = gr.Textbox(label="Transactions", interactive=False)
        transactions_button.click(get_transactions, outputs=transactions_result)

demo.launch()