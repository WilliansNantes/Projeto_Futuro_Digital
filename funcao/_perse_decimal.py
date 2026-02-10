from flask import Flask, Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy #importar certinho
import re


from conf.database import db

def _parse_decimal(value: str) -> float:
    if value is None:
        raise ValueError("Valor vazio")
    s = value.strip()
    s = s.replace('R$', '').replace(' ', '')
    if any(c.isalpha() for c in s):
        raise ValueError("Contém caracteres alfabéticos")

    last_dot = s.rfind('.')
    last_comma = s.rfind(',')

    if last_dot != -1 and last_comma != -1:
        if last_comma > last_dot:
            s = s.replace('.', '')
            s = s.replace(',', '.')
        else:
            s = s.replace(',', '')
    elif last_comma != -1:
        s = s.replace('.', '')
        s = s.replace(',', '.')
    else:
        # only dots or digits
        if last_dot != -1:
            parts = s.split('.')
            if len(parts) > 1 and all(len(p) == 3 for p in parts[1:]):
                s = s.replace('.', '')

    if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", s):
        raise ValueError("Formato numérico inválido")

    return float(s)