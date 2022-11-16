4"""Configs for filter annotation modules"""

# Sample API from viewer/AI studio to fetch all WSIs of a definite type, e.g. Tumor positive
SAMLE_JSON_QUERY_WSI_TYPE = {
    "wsi_type":["Tumor","PCD"],
    "institution":""
}

# Sample API from viewer/AI studio to fetch all WSIs of a definite type, from e.g. Tumor positive
SAMLE_JSON_QUERY_WSI_TYPE_INSTITUTION = {
    "wsi_type":["Tumor","PCD"],
    "institution":["Mayo Clinic"]
}

# Sample API from viewer/AI studio to fetch annotations within a viewport from a single WSI
SAMLE_JSON_QUERY_VIEWPORT = {
    "wsi_name":["2001V401001_55"],
    "label_type":"annotation",
    "magnification":40
    "viewport":((x1,y1),(x2,y2))
    "instance_id":[]
}

# Sample API from viewer/AI studio to fetch nucleus within a viewport from a single WSI
SAMLE_JSON_QUERY_VIEWPORT = {
    "wsi_name":["2001V401001_55"],
    "label_type":"nucleus",
    "magnification":40
    "viewport":((x1,y1),(x2,y2))
    "instance_id":[]
}
    
# Sample API from viewer/AI studio to update annotation points for a single WSI 
SAMLE_JSON_UPDATE = {
    "wsi_name":"2001V401001_55",
    "magnification":40
    "insert":{
        [(850,210,0),(890,200,0)]
    }
    "delete":{
        [(8700,2100,3),(90,20,1)]
    }
}