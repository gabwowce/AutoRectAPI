
def generate_links(
    resource: str,
    resource_id: int | None = None,
    extra: dict[str, str] | None = None,
    actions: list[str] | None = None,
) -> dict[str, dict]:
    """
    Grąžina HAL stiliaus _links žemėlapį.
    ---------
    resource    pvz. 'invoices'
    resource_id jei None – laikoma kolekcija (/invoices)
    extra       susiję resursai: {"order": "/orders/42"}
    actions     leistini veiksmai: ['update', 'delete', 'update_status']
    """
    base = f"/{resource}"
    if resource_id is not None:
        base += f"/{resource_id}"

    links: dict[str, dict] = {"self": {"href": base}}

    if resource_id is None:          # kolekcija
        links["create"] = {"href": f"/{resource}", "method": "POST"}
    else:                            # pavienis resursas
        for act in (actions or []):
            match act:
                case "update":
                    links["update"] = {"href": base, "method": "PUT"}
                case "delete":
                    links["delete"] = {"href": base, "method": "DELETE"}
                case "update_status":
                    links["update_status"] = {"href": f"{base}/status", "method": "PATCH"}

    if extra:
        links.update({rel: {"href": href} for rel, href in extra.items()})
    return links
