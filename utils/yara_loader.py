# import os
# import yara
# from config import YARA_RULES_PATH


# def load_clean_rules(base_path: str = YARA_RULES_PATH):
#     rule_files = {}

#     for namespace in ["malware", "packers", "webshells"]:
#         folder = os.path.join(base_path, namespace)

#         for root, _, files in os.walk(folder):
#             for file in files:
#                 if file.endswith(".yar") or file.endswith(".yara"):
#                     full_path = os.path.join(root, file)

#                     try:
#                         yara.compile(filepath=full_path)
#                         key = f"{namespace}_{file}"
#                         rule_files[key] = full_path

#                     except Exception as e:
#                         print(f"[!] Skipping bad rule: {file} -> {e}")

#     return yara.compile(filepaths=rule_files)



import os
import yara
from config import YARA_RULES_PATH

_RULES_CACHE = None


def load_clean_rules(base_path: str = YARA_RULES_PATH):
    global _RULES_CACHE

    if _RULES_CACHE is not None:
        return _RULES_CACHE

    rule_files = {}

    for namespace in ["malware", "packers", "webshells"]:
        folder = os.path.join(base_path, namespace)

        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".yar") or file.endswith(".yara"):
                    full_path = os.path.join(root, file)

                    try:
                        yara.compile(filepath=full_path)
                        key = f"{namespace}_{file}"
                        rule_files[key] = full_path

                    except Exception as e:
                        print(f"[!] Skipping bad rule: {file} -> {e}")

    _RULES_CACHE = yara.compile(filepaths=rule_files)
    print(f"[+] YARA rules loaded: {len(rule_files)} files compiled")
    return _RULES_CACHE