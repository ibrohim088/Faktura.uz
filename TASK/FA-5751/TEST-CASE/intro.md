#### YUR LITSO -- ***https://test.faktura.uz/ru/document/details/df58b9b12c63430e9e13ddacaefa5c7f***
#### FIZ LITSO -- ***https://test.faktura.uz/ru/document/details/884ad9815da849b4b2742cf27709c521***


### Javascript код для автозаполнение полей
FA-5751 — Uztelekom ijara shartnomasi formasini test ma'lumotlari bilan to'ldirish.
Ishlatish: formani oching (юр. yoki физ.), F12 -> Console -> shu kodni joylashtiring -> Enter.
Kontragent, filial va barcha maydonlar to'ladi; "Сохранить" ni o'zingiz bosasiz.

```
(function () {
    var root = document.querySelector('.add-uztelecom-rent-contract-component');
    if (!root || !root.__vue__) {
        console.error('❌ Forma topilmadi. Договор аренды sahifasida ekaningizga ishonch hosil qiling.');
        return;
    }
    var c = root.__vue__;

    // --- Kontragent (Арендодатель) ---
    var CONTRACTOR_INN = '305395454';
    c.contractorInn = CONTRACTOR_INN;
    c.form.contractorInnDisplay = CONTRACTOR_INN;
    if (c.$refs.contractorSearcher && c.$refs.contractorSearcher.setContractor) {
        c.$refs.contractorSearcher.setContractor(CONTRACTOR_INN, null);
    }
    c.loadContractorCompanyInfo(CONTRACTOR_INN);

    // --- Filial (birinchisini tanlaydi; direktor avtomatik to'ladi) ---
    if (c.ownerFilials && c.ownerFilials.length) {
        c.selectedFilial = c.ownerFilials[0];
    } else {
        c.form.branchName = 'Тошкент шахар филиали';
        c.form.branchDirector = 'XOJAYEV DAVLAT SALAYEVICH';
    }

    // --- Shartnoma sarlavhasi ---
    Object.assign(c.form, {
        contractNumber: 'TEST-001',
        contractDate: '02.09.2026',
        contractCity: 'Ташкент',
        currency: 'сум',
        powerOfAttorneyNumber: 'DOV-15/2026',
        powerOfAttorneyDate: '10.01.2026',

        // Объект аренды
        object1Type: 'Помещение',
        object1Area: '25.5',
        object2Type: 'Помещение',
        object2Area: '29.5',
        objectAddress: 'г. Ташкент, Мирзо-Улугбекский р-н, ул. Тестовая, 7',
        ownershipDocuments: 'Кадастровый паспорт № 11:22:33 от 15.01.2024',

        // Срок аренды
        rentStartDate: '01.09.2026',
        rentEndDate: '31.08.2027',
        firstPaymentMonth: 'сентябрь 2026 г.',
        firstPaymentDate: '10.10.2026',

        // Протокол
        protocolStartDate: '01.09.2026',
        protocolEndDate: '31.08.2027',
        protocolAmount: '42 000 000',
        protocolAmountInWords: 'сорок два миллиона',

        comment: 'FA-5751 test'
    });

    // --- Faqat физ. лицо uchun ---
    if (c.isIndividual) {
        Object.assign(c.form, {
            contractorPinfl: '51234567890123',
            contractorPassportSeries: 'AA1234567',
            contractorPassportIssuedBy: 'ИИБ Мирзо-Улугбекского района г. Ташкента',
            contractorPassportIssueDate: '15.03.2020'
        });
    }

    // --- Стоимость аренды: 3 qator ---
    c.form.rentRows = [
        { address: 'г. Ташкент, ул. Тестовая, 7', areaType: 'Помещение', area: '25.5',
          periodFrom: '01.09.2026', periodTo: '31.08.2027', monthPrice: '1000000', totalPrice: '12000000' },
        { address: 'г. Ташкент, ул. Тестовая, 9', areaType: 'Помещение', area: '29.5',
          periodFrom: '01.09.2026', periodTo: '31.08.2027', monthPrice: '2500000', totalPrice: '30000000' },
        { address: 'г. Ташкент, ул. Тестовая, 11', areaType: 'Антенно-мачтовое сооружение', area: '12',
          periodFrom: '01.09.2026', periodTo: '31.08.2027', monthPrice: '500000', totalPrice: '6000000' }
    ];

    c.$nextTick(function () {
        c.initDatepickers();
        c._syncDocumentTitle();
        console.log('✅ Forma to\'ldirildi.');
        console.log('   Общая площадь :', c.totalArea, '(kutilgan 55)');
        console.log('   ИТОГО в месяц :', c.totalMonthPrice, '(kutilgan 4000000)');
        console.log('   ИТОГО договора:', c.totalPrice, '(kutilgan 48000000)');
        console.log('   Филиал        :', c.form.branchName || '(bo\'sh — qo\'lda tanlang)');
        console.log('   Директор      :', c.form.branchDirector);
        console.log('➡️  Endi "Сохранить" tugmasini bosing.');
    });
})();
```

## TEST - CASE - INTRO

**Для того чтобы начать тест надо сначала было ознакомиться с самим задачей**

```Информация о задаче

Uztelecom uchun ikki xil shartnoma shablonini ishlab chiqish zarur:

    • Jismoniy shaxslar (физлица) uchun
    • Yuridik shaxslar (юрлица) uchun

Shablonlar berilgan shakllar va yuborilgan hujjatlar asosida tayyorlanishi kerak.

Talablar:

    1. Jismoniy shaxslar uchun shartnoma shabloni
        Berilgan shakl va hujjatlar asosida to‘liq shablon tayyorlash.
        Barcha majburiy maydonlar, shartlar va bandlar to‘liq bo‘lishi kerak.

    2. Yuridik shaxslar uchun shartnoma shabloni
        Berilgan shakl va hujjatlar asosida to‘liq shablon tayyorlash.
        Yuridik shaxslarga xos rekvizitlar, mas’uliyat va boshqa maxsus bandlar hisobga olinishi lozim.
    
    3. Umumiy talablar
        Shablonlar tahrir qilinishi mumkin bo‘lgan formatda (Word yoki tizim ichida foydalanish mumkin bo‘lgan shaklda) tayyorlanishi kerak.
        Matnlar aniq, yuridik jihatdan to‘g‘ri va Uztelecom talablariga mos bo‘lishi kerak.

Amalga oshirish talab etiladi

    Yuborilgan hujjatlar va shakllarni tahlil qilish.
    Jismoniy shaxslar uchun shartnoma shablonini ishlab chiqish.
    Yuridik shaxslar uchun shartnoma shablonini ishlab chiqish.
    Shablonlarni tekshirish va kerakli tuzatishlarni kiritish.
    Tayyor shablonlarni topshirish.

Kutilayotgan natija

    Jismoniy shaxslar uchun to‘liq va ishlatishga tayyor shartnoma shabloni.
    Yuridik shaxslar uchun to‘liq va ishlatishga tayyor shartnoma shabloni.
    Shablonlar berilgan shakllarga va yuborilgan hujjatlarga mos keladi.
```

Теперь как мы ознакомились с Задачой надо Теперь поставить темлайты шаблоны для Договора для того чтобы поставить шаблон надо зайти внутрь
"Панель Администратора" потом от туда зайти внутрь "Шаблоны" потом внутрь "Тип Документа" после того как нашли нужную страницу потом
Нажать на кнопку "Добавить" откроется пункт "Добавить новый шаблон документа" тут надо заполнить весь Form

**Короткое Информация о путях**
```
"Панель Администратора" --> "Шаблоны" -->  "Тип Документа" --> "Добавить" ==> "Добавить новый шаблон документа" => "Form"
```

### Form для "Узтелеком Договор аренды (юр. лицо)" и также для "Узтелеком Договор аренды (физ. лицо)" - меняется только Тип Документа
```
    "Тип Документа" : "Узтелеком Договор аренды (юр. лицо)"
    "Тип Шаблона" : "HTML"
    "Файл шаблона" : "сюда надо поставить шаблон которыл был сделан (файл находится внутри UZTELEKOM-FIZ-TEMPLATE) для Физ литса"
    "Файл шаблона" : "сюда надо поставить шаблон которыл был сделан (файл находится внутри UZTELEKOM-YUR-TEMPLATE) для Юр литса"
    "Тип рендера" : "Scriban был выбран"
    "Комментарий" : "Шаблон для Uztelecom"
    "Сохранить" : "Для того чтобы добавить новый шаблон"
```

### Причина потому что был выбран "Тип рендера": "Scriban" а не "Default"
```
Когда выбран был Default происходила такая ошибка что "Стоимость аренды" он не заполнялся, 
так сказал разработчик "Azamjon" что в самом коде это ошибка я для предупреждение написал это
```

### После того как добавили новый шаблон для Uztelekom

Потом заходим в раздел "Организации", не выходя из "Панель Администратора", 
тут выбираем нужную компанию для тестирования "302563857 (\"SPACE ONLINE GENESIS\" MCHJ)"

**Короткое Информация о путях**
```
    "Панель Администратора" --> "Организации" --> "Search" --> "302563857" => "Разрешение компании" => "Документ"
```

Потом заходим в "Разрешение компании", открываем "Документ", внизу будут новые поля:

- [X] Доступ к созданию договора аренды Узтелеком (юр. лицо)
- [X] Доступ к созданию договора аренды Узтелеком (физ. лицо)

Эти поля надо отметить галочкой, чтобы они стали активными.

После того как сделали нужные поля активными надо "Сохранить"


### Выходим с Панеля Администратора попадаем в главное меню 
***https://test.faktura.uz/ru/account/home***
