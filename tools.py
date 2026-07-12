import requests
from langchain_core.tools import tool

from config import DJANGO_API_BASE_URL


@tool
def get_order_status(order_id: str) -> str:
    """Look up the status, total amount, and items of an order by its numeric ID."""
    try:
        resp = requests.get(f"{DJANGO_API_BASE_URL}/orders/{order_id}/", timeout=5)
        if resp.status_code == 404:
            return f"No order found with ID {order_id}."
        resp.raise_for_status()
        data = resp.json()
        items_summary = ", ".join(
            f"{item['quantity']}x {item.get('product_name', 'item')}"
            for item in data.get("items", [])
        )
        return (
            f"Order #{data['id']} is currently '{data['status']}'. "
            f"Total: {data['total_amount']}. "
            f"Items: {items_summary or 'none listed'}."
        )
    except requests.RequestException as exc:
        return f"Could not reach the order service: {exc}"


@tool
def list_customer_orders(customer_id: str) -> str:
    """List all orders belonging to a given customer ID, with status and total."""
    try:
        resp = requests.get(
            f"{DJANGO_API_BASE_URL}/orders/",
            params={"customer": customer_id},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", data if isinstance(data, list) else [])
        if not results:
            return f"No orders found for customer {customer_id}."
        lines = [
            f"Order #{o['id']} - {o['status']} - total {o['total_amount']}"
            for o in results
        ]
        return "\n".join(lines)
    except requests.RequestException as exc:
        return f"Could not reach the order service: {exc}"


@tool
def search_products(query: str) -> str:
    """Search the product catalog by name or description keyword."""
    try:
        resp = requests.get(
            f"{DJANGO_API_BASE_URL}/products/",
            params={"search": query},
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", data if isinstance(data, list) else [])
        if not results:
            return f"No products matched '{query}'."
        lines = [
            f"{p['name']} - ${p['price']} ({p['stock_quantity']} in stock)"
            for p in results
        ]
        return "\n".join(lines)
    except requests.RequestException as exc:
        return f"Could not reach the product service: {exc}"


ALL_TOOLS = [get_order_status, list_customer_orders, search_products]
