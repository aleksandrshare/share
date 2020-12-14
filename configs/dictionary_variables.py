""" Хранилище словарных данных, необходимых для генерации сущностей """

lawEnforcementRequest = ('UNKW', 'POL', 'NPL')
entities_status = ['new', 'inProgress', 'closed']
assistance = ('HLP', 'NND')
vectorCode = ('EXT', 'INT')
serviceType = ('RBS', 'ABS ', 'Front-office', 'Back-office', 'WEB', 'CFS', 'CRBS', 'ECS', 'OTH')
typeOfIncident = ('MTR', 'BAC', 'FMA', 'DT_MTR', 'DT_FS')
#EXT
detectedBy = ('AFR', 'CLNT')
ext_events = ('MTR_WC', 'A_SC', 'UO_WC', 'FMA_WC', 'OTH')
TaMfunds = ('MBB', 'BRW', 'PCW', 'ATM', 'POS', 'SST', 'CNP', 'ABC')
#INT
int_events = ('MTR_UA', 'EMP_UA', 'FMS_UA', 'UPT_PSP', 'UPT_EMP', 'DT_ALL', 'DT_SELECTED', 'DT_PSP', 'DT_SC', 'DTPT_SC',
              'DT_CC', 'DTPT_CC', 'DT_OC')
typeOfIntruder = ('INT_ORG', 'EXT_ORG')

antifraudTransferState = ('unknown', 'rejected', 'confirmed', 'notConfirmed')
antifraudTransferSuspension = ('suspended', 'unableToSuspend')

antifraudType = ('paymentCard', 'phoneNumber', 'eWallet', 'bankAccount', 'other', 'swift', 'retailAtm')
antifraudType2_1 = ('paymentCard', 'phoneNumber', 'eWallet', 'bankAccount', 'other')
currency = ('643', '978', '840', '008', '971')

atmAttacksTarget = ('ATM', 'CIN', 'REC', 'POS', 'SST', 'OTH')
atmAttacksAttackType = ('BBX', 'DSP', 'SKM', 'OTH')
ddosAttacksType = ('icmpFlood', 'ntpAmplification', 'tftpAmplification', 'sentinelAmplification', 'dnsAmplification',
                   'snmpAmplification', 'ssdpAmplification', 'chargenAmplification', 'ripV1Amplification',
                   'bitTorrentAmplification', 'qtpdAmplification', 'quakeAmplification', 'ldapAmplification',
                   'amplification49Ad34', 'portmapAmplification', 'kadAmplification', 'netBiosAmplification',
                   'steamAmplification', 'dpiAttack', 'landAttack', 'tcpSynAttack', 'tcpAckAttack', 'smurfAttack',
                   'icmpUdpFrag', 'tcpFrag', 'sslAttack', 'dnsWaterTortureAttack', 'wordpressPingbackDdos', 'dnsFlood',
                   'httpOrHttpsFlood', 'ftpFlood', 'smtpFlood', 'voipSipAttack', 'pop3Flood', 'slowRateAttack', 'other')

orgType = ('company', 'individual')

# analistic form
cardType = ('credit', 'debit', 'prepaid')
cardProduct = ('campus', 'personal', 'salary', 'corporate')
operationType = ('purchase', 'payment', 'transfer', 'withdrawal', 'commision', 'fine', 'other')

bool_values = (True, False)

counties = {'CZ': '+420', 'RU': '+7', 'MU': '+230', 'TC': '+1 649', 'LV': '+371', 'KZ': '+7 7', 'RO': '+40', 'TM': '+993'}

threat_types = {'MLW': 'Вредоносное программное обеспечение', 'EXP': 'Эксплуатация уязвимости',
                'DOS': 'DDoS', 'BCC': 'ЦУ бот-сети', 'PHI': 'Фишинг', 'MLR': 'Вредоносный ресурс',
                'TEL': 'Мошеннический телефонный номер', 'OTH': 'Другое'}

vulnerability_classes = {'COD': 'Уязвимость кода (COD)',
                         'CFG': 'Уязвимость конфигурации (CFG)',
                         'ARH': 'Уязвимость архитектуры (ARH)',
                         'ORG': 'Организационная уязвимость (ORG)',
                         'MULT': 'Многофакторная уязвимость (MULT)',
                         'OTH': 'Не определенная уязвимость (OTH)'}

vulnerability_types = {'CFG': 'Неправильная настройка параметров ПО',
                       'VLD': 'Неполнота проверки вводимых данных',
                       'PTH': 'Возможность прослеживания пути доступа к каталогам',
                       'LNK': 'Возможность перехода по ссылкам',
                       'CMD': 'Возможность внедрения команд ОС',
                       'CSS': 'Межсайтовый скриптинг',
                       'INJ': 'Внедрение интерпретируемых операторов языков программирования или разметки',
                       'COD': 'Внедрение произвольного кода',
                       'BFR': 'Переполнение буфера памяти',
                       'STR': 'Неконтролируемая форматная строка',
                       'CALC': 'Вычисления',
                       'INFO': 'Утечка/раскрытие информации ограниченного доступа',
                       'ACNT': 'Управление полномочиями',
                       'PRIV': 'Управление разрешениями, привилегиями и доступом',
                       'AUTH': 'Аутентификация',
                       'CRIP': 'Криптографические преобразования',
                       'CSR': 'Подмена межсайтовых запросов',
                       'RCND': 'Приводящий к «состоянию гонки»',
                       'RES': 'Управление ресурсами',
                       'OTH': 'Другое'}
vulnerability_found_in = {'SYS': 'Общесистемное программное обеспечение',
                          'SFW': 'Прикладное программное обеспечение',
                          'SPS': 'Специальное программное обеспечение',
                          'TCH': 'Технические средства',
                          'PRT': 'Портативные технические средства',
                          'NET': 'Сетевое (коммуникационное, телекоммуникационное) оборудование',
                          'SEC': 'Средства защиты информации',
                          'OTH': 'Другое'}

vulnerability_classes_incident = {'COD': 'COD (Уязвимость кода)',
                                  'CFG': 'CFG (Уязвимость конфигурации)',
                                  'ARH': 'ARH (Уязвимость архитектуры)',
                                  'ORG': 'ORG (Организационная уязвимость)',
                                  'MULT': 'MULT (Многофакторная уязвимость)',
                                  'OTH': 'OTH (Не задан)'}
vulnerability_types_incident = {'CFG': 'Неправильная настройка параметров ПО (CFG)',
                                'VLD': 'Неполнота проверки вводимых данных (VLD)',
                                'PTH': 'Возможность прослеживания пути доступа к каталогам (PTH)',
                                'LNK': 'Возможность перехода по ссылкам (LNK)',
                                'CMD': 'Возможность внедрения команд ОС (CMD)',
                                'CSS': 'Межсайтовый скриптинг (CSS)',
                                'COD': 'Возможность внедрения произвольного кода (COD)',
                                'BFR': 'Переполнение буфера памяти (BFR)',
                                'STR': 'Неконтролируемая форматная строка (STR)',
                                'CALC': 'Ошибка вычислений (CALC)',
                                'INFO': 'Утечка/раскрытие информации ограниченного доступа (INFO)',
                                'ACNT': 'Управление полномочиями (ACNT)',
                                'PRIV': 'Управление разрешениями, привилегиями и доступом (PRIV)',
                                'AUTH': 'Аутентификация (AUTH)',
                                'CRIP': 'Криптографические преобразования (CRIP)',
                                'CSR': 'Подмена межсайтовых запросов (CSR)',
                                'RCND': 'Приводящий к «состоянию гонки» (RCND)',
                                'RES': 'Управление ресурсами (RES)',
                                'OTH': 'Другое (OTH)'}
vulnerability_found_in_incident = {'SYS': 'Общесистемное программное обеспечение (SYS)',
                                   'SFW': 'Прикладное программное обеспечение (SFW)',
                                   'SPS': 'Специальное программное обеспечение (SPS)',
                                   'TCH': 'Технические средства (TCH)',
                                   'PRT': 'Портативные технические средства (PRT)',
                                   'NET': 'Сетевое (коммуникационное, телекоммуникационное) оборудование (NET)',
                                   'SEC': 'Средства защиты информации (SEC)',
                                   'OTH': 'Другое (OTH)'}

federal_districts = {'Central': 'Центральный федеральный округ',
                     'South': 'Южный федеральный округ',
                     'NorthWest': 'Северо-Западный федеральный округ',
                     'FarEast': 'Дальневосточный федеральный округ',
                     'Siberia': 'Сибирский федеральный округ',
                     'Ural': 'Уральский федеральный округ',
                     'Volga': 'Приволжский федеральный округ',
                     'Caucas': 'Северо-Кавказский федеральный округ',
                     'Another': 'Другой'}

pub_event_type = {'CNF': 'Конференция',
                  'PBE': 'Публикация на внешнем ресурсе (в т.ч. печатные издания)',
                  'PBI': 'Публикация на собственном ресурсе направляющего информацию (в т.ч. печатные издания)'}

pub_event_type_info_card = {'CNF': '(CNF) Конференция',
                            'PBE': '(PBE) Публикация на внешнем ресурсе (в т.ч. печатные издания)',
                            }
payee_type_2_1 = ['bankAccount', 'paymentCard']
payee_type = ['bankAccount', 'paymentCard', 'retailAtm', 'swift']

send_types = ['trafficHijackAttacks', 'malware', 'ddosAttacks', 'vulnerabilities', 'bruteForces', 'spams',
              'controlCenters', 'phishingAttacks', 'prohibitedContents', 'maliciousResources',
              'changeContent']

prometheus_queries = {'cpu_usage': '100 - (avg(irate(windows_cpu_time_total{mode="idle",%(job_name)s}[2m])) * 100)',
                     'memory_usage':
                         'windows_cs_physical_memory_bytes - windows_os_physical_memory_free_bytes{%(job_name)s}',
                     'disk_c_free': 'windows_logical_disk_free_bytes{volume="C:",%(job_name)s}'}

incident_types = ("Вредоносные ресурсы", "Командный центр бот-сети", "НСД", "Отказ в обслуживании",
               "Подбор данных", "Сканирование сети", "Спам", "Узел бот-сети", "Фишинг",
               "Эксплуатация уязвимости", "Несанкционированное изменение данных",
               "Несанкционированное удаление данных", "Утечка данных", "Использование запрещенных сервисов",
               "Нарушение регламента по установке обновлений", "Превышение служебных полномочий",
               "Установка запрещенного ПО", "Атака типа “Отказ в обслуживании”",
               "Нарушение работоспособности ПО", "Нарушение работоспособности при резервном копировании данных",
               "Нарушение работоспособности сервиса", "Неработоспособность средств защиты",
               "Не определен", "Подозрительные операции с ПО", "Компрометация пользователя",
               "Компрометация узла/ПО", "Нарушение границ внешнего периметра", "Обход средств защиты",
               "Обнаружение вируса", "Обнаружение сетевого червя", "Обнаружение троянской программы",
               "Обнаружение хакерского ПО", "Обнаружение бэкдора", "Обнаружение критически опасной уязвимости")

severity = ('Высокая', 'Средняя', 'Низкая')

influence = ('Потенциальное воздействие на не критически важный актив',
          'Воздействие на не критически важный актив с последующим нарушением целостности',
          'Воздействие на не критически важный актив с последующим нарушением конфиденциальности',
          'Воздействие на критически важный актив, приводящее к финансовым или иным потерям')

mapping__severity = {'High': 'high', 'Medium': 'middle', 'Low': 'low'}
