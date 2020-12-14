#!/usr/bin/env python
# -*- coding: utf-8

from framework.other_proj_ui.ui_auto.locators.fc_locators import LocatorsLKO as locators


# При изменении 1 параметра, находится 1 элемент страницы
participant_data_diff_fields = {
    'orgFullName': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_FULLNAME,
    'orgShortName': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_SHORTNAME,
    'orgLegalEntityForm': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ENTITY_FORM,
    'orgBrand': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_BRAND,
    'orgEmails': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_GROUP_EMAILS,
    'orgIncomingEmail': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_INCOMING_EMAIL,
    'id_cii': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_KII_ID,
    'orgType': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_ORG_TYPE,
    'isp.name': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_MOB_OPERATOR,
    'isp.ipAddress': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_MOB_OPERATOR,
    'orgInn': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_INN,
    'orgKpp': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_KPP,
    'orgOgrn': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_OGRN
}

# При изменении 1 параметра, находится 2 элемента страницы
participant_user_diff_fields = {
    'firstName': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_FIRSTNAME,
    'lastName': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_LASTNAME,
    'middleName': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_MIDDLENAME,
    'accessRights': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_ACCESS_RIGHTS,
    'active': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_IS_ACTIVE,
    'position': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_POSITION,
    'landlineNumber': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_LANDLINE_NUMBER,
    'mobileNumber': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_MOBILE_NUMBER,
    'email': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_EMAIL,
    'certificate.certificateSerialNumber': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_CURRENT_CERT_NUMBER,
    'certificate.certificateValidFrom': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_CURRENT_CERT_VALID_FROM,
    'certificate.certificateValidTo': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_CURRENT_CERT_VALID_ТО,
    'previousCertificate.certificateSerialNumber': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_CURRENT_CERT_NUMBER,
    'previousCertificate.certificateValidFrom': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_CURRENT_CERT_VALID_FROM,
    'previousCertificate.certificateValidTo': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_USER_CURRENT_CERT_VALID_ТО,
    'swiftBikCustomizationBlock': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_SWIFT_BIK,
    'acquirerIdCustomizationBlock': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_ACQUIRER_ID,
    'paymentSystemMemberIdCustomizationBlock': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PAYMENT_SYS_ID,
    'cryptographyCustomizationBlock': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_CRYPTO,
    'facsimileNumberBlockingCorrespondentAccount': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_FAX_NUMBER,
    'webSite': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_WEBSITE,
    'bin': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_BIN,
    'bic': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_BIK

}

# При изменении 1 параметра, находится 2 элемента страницы
participant_address_diff_fields = {
    'legalAddress.oktmo': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_OKTMO,
    'legalAddress.postalCode': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_POSTAL_CODE,
    'legalAddress.country': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_COUNTRY,
    'legalAddress.federalDistrict': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_FEDERAL_DISTRICT,
    'legalAddress.subjectOfFederation': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_SUBJ_OF_FEDERATION,
    'legalAddress.district': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_DISRICT,
    'legalAddress.city': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_CITY,
    'legalAddress.cityDistrict': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_CITY_DISTRICT,
    'legalAddress.locality': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_LOCALITY,
    'legalAddress.street': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_STREET,
    'legalAddress.house': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_HOUSE,
    'legalAddress.building': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_BUILDING,
    'legalAddress.room': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_ROOM,
    'legalAddress.additionalInformation': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_ADDINFO,
    'legalAddress.fiasId': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_LEGAL_ADDRESS_FIAS_ID,
    'postAddress.oktmo': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_OKTMO,
    'postAddress.postalCode': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_POSTAL_CODE,
    'postAddress.country': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_COUNTRY,
    'postAddress.federalDistrict': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_FEDERAL_DISTRICT,
    'postAddress.subjectOfFederation': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_SUBJ_OF_FEDERATION,
    'postAddress.district': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_DISRICT,
    'postAddress.city': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_CITY,
    'postAddress.cityDistrict': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_CITY_DISTRICT,
    'postAddress.locality': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_LOCALITY,
    'postAddress.street': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_STREET,
    'postAddress.house': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_HOUSE,
    'postAddress.building': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_BUILDING,
    'postAddress.room': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_ROOM,
    'postAddress.additionalInformation': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_ADDINFO,
    'postAddress.fiasId': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_POST_ADDRESS_FIAS_ID,
    'physicalAddress.oktmo': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_OKTMO,
    'physicalAddress.postalCode': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_POSTAL_CODE,
    'physicalAddress.country': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_COUNTRY,
    'physicalAddress.federalDistrict': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_FEDERAL_DISTRICT,
    'physicalAddress.subjectOfFederation': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_SUBJ_OF_FEDERATION,
    'physicalAddress.district': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_DISRICT,
    'physicalAddress.city': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_CITY,
    'physicalAddress.cityDistrict': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_CITY_DISTRICT,
    'physicalAddress.locality': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_LOCALITY,
    'physicalAddress.street': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_STREET,
    'physicalAddress.house': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_HOUSE,
    'physicalAddress.building': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_BUILDING,
    'physicalAddress.room': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_ROOM,
    'physicalAddress.additionalInformation': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_ADDINFO,
    'physicalAddress.fiasId': locators.MW_VIEW_PARTICIPANT_LKO_DIFF_PHYSICAL_ADDRESS_FIAS_ID
}
