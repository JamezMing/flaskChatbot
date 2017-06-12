import tensorflow as tf
import nltk
import numpy as np

# preprocessed data
import data
import data_utils

class SeqProcessor:
    def __init__(self, path = "/home/james/PycharmProjects/flaskChatbot/app/seq2seq_backend/seq2seq_model.ckpt-44000"):
        self.metadata, self.idx_q, self.idx_a = data.load_data(PATH='/home/james/PycharmProjects/flaskChatbot/app/seq2seq_backend/datasets/cornell_corpus/')
        self.path = path
        (trainX, trainY), (testX, testY), (validX, validY) = data_utils.split_dataset(self.idx_q, self.idx_a)

        # parameters
        xseq_len = trainX.shape[-1]
        yseq_len = trainY.shape[-1]
        batch_size = 32
        xvocab_size = len(self.metadata['idx2w'])
        yvocab_size = xvocab_size
        emb_dim = 1024

        import seq2seq_wrapper

        # In[7]:

        self.model = seq2seq_wrapper.Seq2Seq(xseq_len=xseq_len,
                                        yseq_len=yseq_len,
                                        xvocab_size=xvocab_size,
                                        yvocab_size=yvocab_size,
                                        ckpt_path='ckpt/cornell_corpus/',
                                        emb_dim=emb_dim,
                                        num_layers=3
                                        )
        self.sess = tf.Session()
        saver = tf.train.Saver()
        saver.restore(self.sess, self.path)



    def process_line(self, line):
        dic = self.metadata['w2idx']
        dic2 = self.metadata['idx2w']
        en = data.process_line(line, dic).reshape((25, 1))
        res = self.model.predict(self.sess, en)
        en2 = data_utils.decode(res[0], dic2)
        res2 = ""
        for word in en2:
            res2 = res2 + word + " "
        return res2