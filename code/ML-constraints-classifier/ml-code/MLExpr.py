from imblearn.over_sampling import SMOTE
import os

class MLExpr:
    def __init__(self,
                 df,
                 models,
                 use_frag,
                 use_sent,
                 use_dispat,
                 use_op,
                 use_ct,
                 debug=False,
                 smote_ratio=1.0,
                 best_param=None,
                 df_=None,
                 mode=None):
        self.df = df
        self.models = models
        self.use_frag = use_frag
        self.use_sent = use_sent
        self.use_dispat = use_dispat
        self.debug = debug
        self.smote_ratio = smote_ratio
        self.use_op = use_op
        self.use_ct = use_ct
        if smote_ratio is None:
            self.smote = None
        else:
            self.smote = SMOTE(sampling_strategy=smote_ratio, k_neighbors=5)
        self.configs = self.set_configs()
        self.best_param = best_param
        self.df_ = df_
        self.mode = mode

    def set_configs(self):
        return [','.join([m[:3] for m in self.models]), 'smote(ratio={})'.format(self.smote_ratio)] + self.get_features_arr()

    def get_features_arr(self):
        arr = []
        if self.use_frag: arr.append('frag')
        if self.use_sent: arr.append('sent')
        if self.use_dispat: arr.append('dispat')
        if self.use_op: arr.append('ops')
        if self.use_ct: arr.append('constype')
        return arr

    def get_out_dir(self, out_dir):
        return os.path.join(out_dir, '_'.join(self.configs))

    def get_crossys_dir(self, data_dir):
        configs = list(self.configs[1:])
        return os.path.join(data_dir, '_'.join(configs))

    def __str__(self):
        return f"model({self.models}), use_frag({self.use_frag}), use_sent({self.use_sent}), use_dispat({self.use_dispat}), debug({self.debug}), use_operands({self.use_op}), use_ct({self.use_ct}), smote_ratio({self.smote_ratio})"