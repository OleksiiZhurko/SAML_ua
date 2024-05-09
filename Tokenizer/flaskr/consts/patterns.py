stop_words: list[str] = [
    'або', 'адже', 'аж', 'алло', 'б', 'безперервно', 'би', 'близько', 'був', 'буває', 'буде',
    'будемо', 'будете', 'будеш', 'буду', 'будуть', 'була', 'були', 'було', 'бути', 'більш',
    'більше', 'вам', 'вами', 'вас', 'ваш', 'ваша', 'ваше', 'вашим', 'вашими', 'ваших', 'вашого',
    'вашому', 'вашою', 'вашої', 'вашу', 'ваші', 'вашій', 'вгору', 'вгорі', 'вдалині', 'весь', 'вже',
    'ви', 'вниз', 'внизу', 'вона', 'вони', 'воно', 'восьмий', 'всею', 'всього', 'всьому', 'всю',
    'вся', 'всім', 'всіх', 'втім', 'відсотків', 'він', 'вісім', 'вісімнадцятий', 'вісімнадцять',
    'г', 'говорив', 'говорить', 'давно', 'далеко', 'далі', 'два', 'двадцятий', 'двадцять',
    'дванадцятий', 'дванадцять', 'двох', 'дві', 'де', "дев'ятий", "дев'ятнадцятий", "дев'ятнадцять",
    "дев'ять", 'декілька', 'десятий', 'десять', 'дня', 'дійсно', 'е', 'ж', 'же', 'завжди',
    'зазвичай', 'зараз', 'звичайно', 'звідси', 'звідусіль', 'значить', 'знову', 'зовсім', 'зі', 'й',
    'його', 'йому', 'каже', 'ким', 'кого', 'кожен', 'кожна', 'кожне', 'кожні', 'коли', 'кому',
    'куди', 'кілька', 'лише', 'м', 'мене', 'менш', 'мені', 'ми', 'мимо', 'мною', 'мого', 'може',
    'можна', 'можуть', 'мою', 'моя', 'моє', 'моєму', 'моєю', 'моєї', 'мої', 'моїй', 'моїм', 'моїми',
    'моїх', 'міг', 'мій', 'мільйонів', 'на', 'навколо', 'навкруги', 'навіщо', 'нагорі', 'назад',
    'нам', 'нами', 'нас', 'наш', 'наша', 'наше', 'нашим', 'нашими', 'наших', 'нашого', 'нашому',
    'нашою', 'нашої', 'нашу', 'наші', 'нашій', 'небагато', 'небудь', 'недалеко', 'нерідко',
    'нещодавно', 'нею', 'неї', 'нибудь', 'нижче', 'низько', 'ним', 'ними', 'них', 'ну', 'нього',
    'ньому', 'ніби', 'ній', 'нім', 'нічого', 'о', 'обидва', 'обоє', 'один', 'одинадцятий',
    'одинадцять', 'однак', 'одного', 'одній', 'однієї', 'означає', 'он', 'особливо', 'ось',
    "п'ятий", "п'ятнадцятий", "п'ятнадцять", "п'ять", 'перед', 'по', 'подів', 'поки', 'пора',
    'поруч', 'посеред', 'потрібно', 'потім', 'почала', 'початку', 'при', 'просто', 'пізніше', 'пір',
    'після', 'раз', 'разу', 'раніше', 'раптом', 'роки', 'року', 'років', 'році', 'рік', 'сама',
    'самих', 'само', 'самого', 'самому', 'самі', 'свого', 'свою', 'своє', 'своєї', 'свої', 'своїй',
    'своїх', 'себе', 'сих', 'сказав', 'сказала', 'скрізь', 'скільки', 'собою', 'собі', 'спочатку',
    'став', 'суть', 'сьогодні', 'сьомий', 'сім', 'сімнадцятий', 'сімнадцять', 'т', 'та', 'так',
    'така', 'таке', 'такий', 'також', 'такі', 'там', 'твого', 'твою', 'твоя', 'твоє', 'твоєму',
    'твоєю', 'твоєї', 'твої', 'твоїй', 'твоїм', 'твоїми', 'твоїх', 'твій', 'те', 'тебе', 'теж',
    'тепер', 'ти', 'тим', 'тими', 'тисяч', 'тих', 'тобою', 'тобі', 'того', 'тоді', 'той', 'тому',
    'тою', 'три', 'тринадцятий', 'тринадцять', 'трохи', 'ту', 'туди', 'тут', 'ті', 'тій', 'тім',
    'тією', 'тієї', 'уміти', 'усього', 'усьому', 'усю', 'усюди', 'уся', 'усі', 'усім', 'усіма',
    'усіх', 'хоч', 'хоча', 'хочеш', 'хто', 'хіба', 'це', 'цей', 'цим', 'цими', 'цих', 'цього',
    'цьому', 'цю', 'ця', 'ці', 'цій', 'цієї', 'часто', 'частіше', 'четвертий', 'чи', 'чий',
    'чийого', 'чийому', 'чим', 'численна', 'численне', 'численний', 'численні', 'чию', 'чия', 'чиє',
    'чиєму', 'чиєї', 'чиї', 'чиїй', 'чиїм', 'чиїми', 'чиїх', 'чотири', 'чотирнадцятий',
    'чотирнадцять', 'шостий', 'шістнадцятий', 'шістнадцять', 'шість', 'ще', 'що', 'щодо', 'щось',
    'я', 'яка', 'який', 'яких', 'якого', 'якої', 'якщо', 'які', 'якій', 'і', 'із', 'іноді', 'інша',
    'інше', 'інших', 'інші', 'їй', 'їм', 'їх', 'її', 'г', 'р'
]

urlPattern: str = r"((http://)[^ ]*|(https://)[^ ]*|(www\.)[^ ]*)"
userPattern: str = r"@[^\s]+"
hashtagPattern: str = r"#[^\s]+"
emailPattern: str = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
phonePattern: str = r'\+?\d[\d\s\-\(\)]{8,}\d'
alphaPattern: str = r"[^a-zA-Z <>АаБбВвГгҐґДдЕеЄєЖжЗзИиІіЇїЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЬьЮюЯя]"
sequencePattern: str = r"(.)\1{3,}"
tabPattern: str = r"\t"
rPattern: str = r"\r"
newLinePattern: str = r"\n"
spacePattern: str = r" {2,}"

seqReplacePattern: str = r"\1\1\1"