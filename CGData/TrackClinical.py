
import CGData
import re


class TrackClinical(CGData.CGMergeObject):

    DATA_FORM = None

    typeSet = { 
        'clinicalMatrix' : True, 
        'clinicalFeature' : True
    } 

    def __init__(self):
        CGData.CGMergeObject.__init__(self)
            
    def get_name( self ):
        return "%s" % ( self.members[ "clinicalMatrix" ].get_name() )
    
    def gen_sql_heatmap(self, id_table):
        CGData.log("ClincalTrack SQL " + self.get_name())

        features = self.members["clinicalFeature"].features
        matrix = self.members["clinicalMatrix"]

        # e.g. { 'HER2+': 'category', ...}
        explicit_types = dict((f, features[f]['valueType']) for f in features if 'valueType' in features[f])

        matrix.feature_type_setup(explicit_types)
        for a in features:
            if "stateOrder" in features[a]:

                #this weird bit of code is to split on ',', but respect \,
                #if you can think of a better way, please replace this
                tmp = re.split(r'([^,]),', features[a]["stateOrder"][0])
                enums = []
                word = True
                appending = False
                e = 0
                while e < len(tmp): 
                    if word:
                        if appending:
                            enums[-1] += tmp[e]
                        else:
                            enums.append(tmp[e])
                        word = False
                    else:
                        if tmp[e] != "\\":
                            enums[-1] += tmp[e]
                            appending = False
                        else:
                            enums[-1] += ","
                            appending = True
                        word = True
                    e += 1
                
                i = 0
                for e in matrix.enum_map[a]:
                    if e in enums:
                        matrix.enum_map[a][e] = enums.index(e)
                    else:
                        matrix.enum_map[a][e] = len(enums) + i
                        i += 1
        for a in matrix.gen_sql_heatmap(id_table, features=features):
            yield a
    
