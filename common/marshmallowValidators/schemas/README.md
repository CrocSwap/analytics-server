Validation schemas for serialization (responces to frontend)

### The structure for these is 
commonValidators house validations used through out most schemas
Each schema has a main shell schema that contains the "Data" sub schema within
this is due to the frontend expecting a structure of:
{
    "data":<schema>
}

###for each schema there are a few variations of the fields within:
`# 'Required'` is the most strict validators, the field can NOT be None/Null and must exist
`# Conditional 'Required'` means the field must exist under certain conditions. mixed bacg of None/Null based on conditional validation requirements
`# Not 'Required'` means the field can not exist alltogether and validation will PASS. However these can NOT be None/Null
`# Not 'Required' can be null` same as above but now fields can also be None/Null
`# Verbose` this is a section of fields that may be removed later. they are not used by anything and are returned "because we had them" digital level hording. no validation should be preformed on these and they should be allowed to be null. ONLY the type must match.