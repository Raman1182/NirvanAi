from . import bible, buddhist, stoicism

def apply_plugin(domain, prompt):
    try:
        plugin = globals()[domain]
        return plugin.preprocess(prompt)
    except Exception:
        return prompt