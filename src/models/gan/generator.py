import tensorflow as tf

from src.models.gan import generator_collection as gencol
from src.models.gan import utils


def get_maxdepthlen():
    return 2*2*2*2*2*3*3 # 288


class BaseGenerator(tf.keras.Model):

    def __init__(self, depthlen, pd_maxdata, ed_maxdata, pd_feature_list=None,
                 ed_feature_list=None, numparticle=6, **kwargs):
        super().__init__(**kwargs)

        self.depthlen = depthlen
        self.maxdepthlen = get_maxdepthlen()
        self.pd_maxdata = pd_maxdata
        self.ed_maxdata = ed_maxdata
        self._numparticle = numparticle

        self.datasplitter = utils.DataSplitter(pd_feature_list,
                                               ed_feature_list)

        self.denormalizer = utils.DataDenormalizer(self.pd_maxdata,
                                                   self.ed_maxdata)

        self.gen_features = self.datasplitter.gen_features

        self.dense_generator = gencol.DenseGenerator(self.maxdepthlen,
                                                     self.gen_features,
                                                     self._numparticle)

        self.oldr_generator = gencol.OldReducedGenerator(self.maxdepthlen,
                                                         self.gen_features,
                                                         self._numparticle)

        self.dense_generator_norm = gencol.DenseGeneratorNorm(self.maxdepthlen,
                                                              self.gen_features,
                                                              self._numparticle)

        self.oldr_generator_norm = gencol.OldReducedGeneratorNorm(self.maxdepthlen,
                                                                  self.gen_features,
                                                                  self._numparticle)

    @tf.function
    def call(self, inputs, training=False):
        label = inputs[0]
        noise = inputs[1:]

        # run different generators
        output1 = self.dense_generator([label,noise,])
        output2 = self.oldr_generator([label,noise,])
        output3 = self.dense_generator_norm([label,noise,])
        output4 = self.oldr_generator_norm([label,noise,])

        # merge outputs
        tensor = output1 + output2 + output3 + output4

        # format data
        tensor = tensor[:,0:self.depthlen,:]
        data = self.datasplitter(tensor)
        data = self.denormalizer(data)

        return data

