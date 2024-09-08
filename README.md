# Səhm Bazarı Analiz Botu

Bu sosial media platformalarından (Reddit və Twitter) səhmlər haqqında məlumatları toplayan, təhlil edən və ümumiləşdirən bir botdur. Bot məlumatların toplanması üçün Reddit və Twitter API-lərindən istifadə edir, onları GPT-4o ilə təhlil edir və ətraflı hesabat tərtib edir.

## Xüsusiyyətləri

- Reddit və Twitter-dən səhm tikerlərin və şərhlərin toplanması
- Məlumatların filtrlənməsi və təmizlənməsi
- Populyar tikerlərin müəyyən edilməsi və etibarlılığının yoxlanılması
- GPT-4o istifadə edərək bazar əhval-ruhiyyəsinin təhlili
- Hər bir tiker üçün ətraflı hesabatların hazırlanması
- Nəticələrin Markdown formatında saxlanması

## Tələblər

- Python 3.7+
- pip (Python paket meneceri)

## Quraşdırma

1. Repozitoriyanı clone edin:
   ```
   git clone https://github.com/vrashad/gpt_finance_assistant.git
   cd gpt_finance_assistant
   ```

2. Asılılıqları quraşdırın:
   ```
   pip install -r requirements.txt
   ```

## Konfiqurasiya

### Reddit API-nin konfiqurasiyası

1. [Reddit App Preferences](https://ssl.reddit.com/prefs/apps) səhifəsinə keçin
2. "Create App" və ya "Create Another App" düyməsini basın
3. Lazımi məlumatları doldurun:
   - Name: Tətbiqinizin adı
   - App type: "script" seçin
   - Description: Botunuzun qısa təsviri
   - About URL: Boş buraxıla bilər
   - Redirect URI: http://localhost:8080
4. "Create app" düyməsini basın
5. "client_id" (tətbiqin adının altında) və "client_secret" qeyd edin

`config.py` faylını yeniləyin:
```python
REDDIT_CLIENT_ID = 'your_client_id'
REDDIT_CLIENT_SECRET = 'your_client_secret'
REDDIT_USER_AGENT = 'your_user_agent_name'
```

### Twitter API-nin konfiqurasiyası

1. [RapidAPI](https://rapidapi.com/) saytında qeydiyyatdan keçin
2. [Twitter API v2](https://rapidapi.com/restocked-gAGxip8a_/api/twitter-api47) üçün abunə olun
3. API açarınızı əldə edin

`config.py` faylını yeniləyin:
```python
RAPIDAPI_KEY = 'your_rapidapi_key'
RAPIDAPI_HOST = 'twitter-api47.p.rapidapi.com'
```

### OpenAI API-nin konfiqurasiyası

1. [OpenAI](https://openai.com/) saytında qeydiyyatdan keçin
2. API açarı əldə edin

`config.py` faylını yeniləyin:
```python
GPT_API_KEY = 'your_openai_api_key'
GPT_BASE_URL = '[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)'  # və ya başqa URL istifadə edirsinizsə
GPT_MODEL = 'gpt-4o'
```

## İşə salma

Botu işə salmaq üçün aşağıdakı əmri yerinə yetirin:

```
python main.py
```

Bot Reddit və Twitter-dən məlumatları toplamağa başlayacaq, onları təhlil edəcək və `config.py`-da göstərilən `OUTPUT_FILE_PATH`-də hesabat tərtib edəcək.

## Proyektin strukturu

- `main.py`: Botu işə salmaq üçün əsas skript
- `config.py`: API parametrləri və digər konfiqurasiyalar üçün fayl
- `reddit.py`: Reddit API ilə işləmək üçün modul
- `twitter.py`: Twitter API ilə işləmək üçün modul
- `utils.py`: GPT-4o ilə əlaqə üçün köməkçi funksiyalar
- `report_generator.py`: Yekun hesabatın tərtib edilməsi üçün modul

## Asılılıqlar

- praw: Reddit API ilə işləmək üçün
- requests: HTTP sorğuları üçün
- openai: GPT-4 API ilə işləmək üçün
- yfinance: Səhmlər haqqında məlumat almaq üçün


## Lisenziya

[MIT Lisenziyası](LICENSE)
