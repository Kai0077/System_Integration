import random
import string
import base64


random_string = "".join(random.choices(string.ascii_letters + string.digits, k=16))
print("RANDOM", random_string)

encoded_string = base64.b64encode(random_string.encode("utf-8")).decode("utf-8")
print("ENCODED", encoded_string)

decoded_string = base64.b64decode(encoded_string).decode("utf-8")
print("DECODED", decoded_string)
