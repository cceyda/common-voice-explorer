from datasets import load_dataset

def cache_dataset(language,split=None):
    dat=load_dataset("common_voice",language,split=split)
    if split:
        return pd.DataFrame(dat)
    else:
        return dat

language_codes=['ab', 'ar', 'as', 'br', 'ca', 'cnh', 'cs', 'cv', 'cy', 'de', 'dv', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'fy-NL', 'ga-IE', 'hi', 'hsb', 'hu', 'ia', 'id', 'it', 'ja', 'ka', 'kab', 'ky', 'lg', 'lt', 'lv', 'mn', 'mt', 'nl', 'or', 'pa-IN', 'pl', 'pt', 'rm-sursilv', 'rm-vallader', 'ro', 'ru', 'rw', 'sah', 'sl', 'sv-SE', 'ta', 'th', 'tr', 'tt', 'uk', 'vi', 'vot', 'zh-CN', 'zh-HK', 'zh-TW']

pool = Pool(processes=len(language_codes))

pool.map(cache_dataset, language_codes)
