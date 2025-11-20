"""Minimal Supabase helper utilities.

This module provides lightweight helpers to sign up and verify Supabase
JWTs using the Supabase Auth REST endpoints. It intentionally avoids a
third-party Supabase client to keep dependencies small.
"""

from __future__ import annotations

import os
from typing import Optional

import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


def is_enabled() -> bool:
    return bool(SUPABASE_URL and SUPABASE_ANON_KEY)


def signup(email: str, password: str) -> dict:
    """Sign up a new user via Supabase Auth.

    Returns the JSON response from Supabase (may include access_token).
    Raises requests.HTTPError for non-2xx responses.
    """
    assert is_enabled(), "Supabase not configured"
    url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/signup"
    headers = {"apikey": SUPABASE_ANON_KEY, "Content-Type": "application/json"}
    resp = requests.post(url, json={"email": email, "password": password}, headers=headers)
    resp.raise_for_status()
    return resp.json()


def sign_in(email: str, password: str) -> dict:
    """Sign in via Supabase Auth (password grant)."""
    assert is_enabled(), "Supabase not configured"
    url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/token?grant_type=password"
    headers = {"apikey": SUPABASE_ANON_KEY, "Content-Type": "application/json"}
    resp = requests.post(url, json={"email": email, "password": password}, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_user_from_token(token: str) -> Optional[dict]:
    """Return Supabase user info for a given access token, or None if invalid."""
    if not is_enabled():
        return None
    url = f"{SUPABASE_URL.rstrip('/')}/auth/v1/user"
    headers = {"Authorization": f"Bearer {token}", "apikey": SUPABASE_ANON_KEY}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    return None
