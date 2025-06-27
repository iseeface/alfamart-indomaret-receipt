import random, string

def format_rupiah(value):
    return f"{value:,.0f}".replace(",", ".")

def generate_npwp():
    return f"{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(1,9)}-{random.randint(100,999)}.{random.randint(100,999)}"

def generate_bon():
    return f"CG{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(1000,9999)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.randint(10,99)}"
