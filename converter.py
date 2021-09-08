import csv
import json
import os
import pandas as pd
import fhirclient.models.bundle
import fhirclient.models.specimen as s
import fhirclient.models.patient as p
import fhirclient.models.fhirreference as r
import fhirclient.models.extension as e
import fhirclient.models.codeableconcept as c
import fhirclient.models.coding
import fhirclient.models.humanname as hn

def createFhir(sourceFile, blueprint):
    bundle = fhirclient.models.bundle.Bundle()
    bundle.type = "transaction"
    bundle.resource_type = "Bundle"
    file = open(blueprint)
    headers = json.load(file)
    headers_dict = dict(headers)
    resources = []
    ids = []
    df = pd.read_csv(sourceFile, usecols=list(dict(headers).values()), sep=';')
    for row in range(len(df.index)):
        p_entry = fhirclient.models.bundle.BundleEntry()
        extension = e.Extension()
        extension.url = "https://fhir.bbmri.de/StructureDefinition/SampleDiagnosis"
        vcc = c.CodeableConcept()
        coding = fhirclient.models.coding.Coding()
        coding.code = "C78"
        coding.system = "http://hl7.org/fhir/sid/icd-10"
        vcc.coding = [coding]
        extension.valueCodeableConcept = vcc
        patient = p.Patient()
        patient.id = str(df[headers_dict.get("personID")].iloc[row])
        p_entry.fullUrl = "http://example.com/Patient/" + str(patient.id)
        bundle_request = fhirclient.models.bundle.BundleEntryRequest()
        bundle_request_specimen = fhirclient.models.bundle.BundleEntryRequest()
        bundle_request_specimen.method = "DELETE"
        bundle_request.method = "DELETE"
        bundle_request.url = "Patient/" + str(patient.id)
        p_entry.request = bundle_request
        p_entry.resource = patient
        if patient.id not in ids:
            ids.append(patient.id)
            resources.append(p_entry)
        s_entry = fhirclient.models.bundle.BundleEntry()
        specimen = s.Specimen()
        specimen.id = str(df[headers_dict.get("sampleID")].iloc[row])
        bundle_request_specimen.url = "Specimen/" + str(specimen.id)
        s_entry.fullUrl = "http://example.com/Specimen/" + str(specimen.id)
        reference = r.FHIRReference()
        reference.reference = "Patient/" + str(patient.id)
        specimen.subject = reference
        specimen.extension = [extension]
        s_entry.resource = specimen
        s_entry.request = bundle_request_specimen
        resources.append(s_entry)
    bundle.entry = resources
    fhir = open("/Users/radot/Projects/ETL/FHIRs/export.json", "w")
    json.dump(bundle.as_json(), fhir)
    print(bundle.as_json())
    fhir.close()



#createFhir('/Users/radot/Projects/ETL/static/riad.csv', '/Users/radot/Projects/ETL/Blueprints/b1.json')