import pprint
import re
import time

import html2text
from textblob import TextBlob
import requests



beds = "https://www.covidbedmbmc.in/HospitalInfo/show"
icu_beds = "https://coronabeds.jantasamvad.org/all-covid-icu-beds.html"


def bed_availability(beds):
    data = html2text.html2text(requests.get(beds).text)
    time.sleep(2)
    blob = TextBlob(data)

    x = blob.split("####")

    j = [i for i in x if i.startswith(" **")]
    extract_out = []
    for hospital in j:
        try:
            contact = re.findall("[0-9]{10}", hospital)[0]
        except IndexError:
            contact = None
        hospital_name = hospital.split("\n")[0].replace('*', '')
        vacant_index = hospital.split("\n").index('Vacant')
        icu_vacant_index = hospital.split("\n").index('ICU Vacant')
        non_icu_vacant_index = hospital.split("\n").index('Non ICU Vacant')


        vacant = hospital.split("\n")[vacant_index - 2].replace('*', '').replace(' ', '').replace('_', '')
        icu_vacant = hospital.split("\n")[icu_vacant_index - 2].replace('*', '').replace(' ', '').replace('_', '')
        non_icu_vacant = hospital.split("\n")[non_icu_vacant_index - 2].replace('*', '').replace(' ', '').replace('_',
                                                                                                                  '')

        extract_out.append((hospital_name, contact, int(vacant), int(icu_vacant), int(non_icu_vacant)))
    return extract_out


if __name__ == "__main__":
    extract_out = bed_availability(beds)
    pprint.pprint(extract_out)
    for i in extract_out:
        if i[1] is not None:
            print('''Hospital: {}
Contact: {}
Total Vacant: {}
ICU Vacant: {}
Non ICU Vacant: {}'''.format(i[0], i[1], i[2], i[3], i[4]))

            print("*" * 50)
