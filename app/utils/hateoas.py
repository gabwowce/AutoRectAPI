# utils/hateoas.py
from typing import Optional, Dict, List


def generate_links(
    resource: str,
    resource_id: Optional[int] = None,
    extra: Optional[Dict[str, str]] = None,
    actions: Optional[List[str]] = None,
) -> Dict[str, Dict[str, str]]:
    """
    Sugeneruoja HAL stiliaus _links žemėlapį.

    :param resource: Pvz. 'invoices'
    :param resource_id: Jei None – laikoma kolekcija (/invoices), kitu atveju – /invoices/{id}
    :param extra: Susiję resursai – {'order': '/orders/42'}
    :param actions: ["update", "delete", "update_status"] ir pan.
    """
    base = f"/{resource}"
    if resource_id is not None:
        base += f"/{resource_id}"

    links: Dict[str, Dict[str, str]] = {"self": {"href": base}}

    if resource_id is None:  # kolekcija
        links["create"] = {"href": f"/{resource}", "method": "POST"}
    else:                    # vienas objektas
        for act in actions or []:
            match act:
                case "update":
                    links["update"] = {"href": base, "method": "PUT"}
                case "delete":
                    links["delete"] = {"href": base, "method": "DELETE"}
                case "update_status":
                    links["update_status"] = {
                        "href": f"{base}/status",
                        "method": "PATCH",
                    }

    if extra:
        links.update({rel: {"href": href} for rel, href in extra.items()})
    return links

