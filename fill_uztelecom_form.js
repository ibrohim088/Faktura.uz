/* FA-5751 — Uztelekom ijara shartnomasi formasini test ma'lumotlari bilan to'ldirish.
   Ishlatish: formani oching (юр. yoki физ.), F12 -> Console -> shu kodni joylashtiring -> Enter.
   Kontragent, filial va barcha maydonlar to'ladi; "Сохранить" ni o'zingiz bosasiz. */
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
