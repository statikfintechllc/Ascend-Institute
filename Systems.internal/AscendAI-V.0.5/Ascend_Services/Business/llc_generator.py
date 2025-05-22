import os
import json
from datetime import datetime

LLC_TEMPLATE = {
    "business_name": "",
    "state": "",
    "owner_name": "",
    "address": "",
    "email": "",
    "formation_date": "",
    "purpose": "",
    "manager_managed": True,
    "registered_agent": {"name": "", "address": ""},
}


def generate_llc_form(
    business_name,
    state,
    owner_name,
    address,
    email,
    purpose="AI-assisted operations and trading infrastructure",
    registered_agent=None,
):
    form = LLC_TEMPLATE.copy()
    form["business_name"] = business_name
    form["state"] = state.upper()
    form["owner_name"] = owner_name
    form["address"] = address
    form["email"] = email
    form["formation_date"] = datetime.utcnow().strftime("%Y-%m-%d")
    form["purpose"] = purpose

    if registered_agent:
        form["registered_agent"] = registered_agent

    filename = f"{business_name}_LLC_Articles_{state}.json"
    with open(filename, "w") as f:
        json.dump(form, f, indent=4)

    print(f"[LLC] Generated formation document: {filename}")
    return filename


if __name__ == "__main__":
    # Example run
    generate_llc_form(
        business_name="Ascend Sovereign Systems",
        state="KS",
        owner_name="Daniel Morris",
        address="235 E 12th Apt. 2, Junction City, KS 66441",
        email="statiksmoktm@gmail.com",
        registered_agent={
            "name": "Northwest Registered Agent, LLC",
            "address": "5909 NW Expressway, Suite 162, Oklahoma City, OK 73132",
        },
    )
