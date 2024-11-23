import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler


class Model(nn.Module):
    def __init__(self, args, data):
        super(Model, self).__init__()
        self.use_cuda = args['cuda']
        self.P = args['window']               # tau
        self.m = data['m']                    # data size [n,m]
        self.hidR = args['hidRNN']            # number of RNN hidden units
        self.hidC = args['hidCNN']            # number of CNN hidden units, number of filter
        self.hidS = args['hidSkip']           # number of skip-RNN hidden units
        self.Ck = args['CNN_kernel']          # kernel size of CNN
        self.skip = args['skip']              # number of cell that skip through
        self.pt = int((self.P - self.Ck)/self.skip)     # times of skips
        self.hw = args['highway_window']
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=self.hidC, kernel_size=(self.Ck, self.m))
        self.GRU1 = nn.GRU(input_size=self.hidC, hidden_size=self.hidR)
        self.dropout = nn.Dropout(p=args['dropout'])
        self.model = args['model']
        self.scale = np.sqrt(self.hidR)
        self.attn = args['attn_score']

        if self.model == 'skip':
            self.GRUskip = nn.GRU(input_size=self.hidC, hidden_size=self.hidS)
            self.linear1 = nn.Linear(in_features=self.hidR + self.skip * self.hidS, out_features=self.m)
        elif self.model == 'attn':
            self.multihead = None
            if self.attn == 'multihead':
                self.multihead = nn.MultiheadAttention(embed_dim=self.hidR, num_heads=5)
            self.linear1 = nn.Linear(in_features=self.hidR * 2, out_features=self.m)
        else:
            self.linear1 = nn.Linear(in_features=self.hidR, out_features=self.m)

        if self.hw > 0:
            self.highway = nn.Linear(in_features=self.hw, out_features=1)
        self.output = None
        if args['output_fun'] == 'sigmoid':
            self.output = torch.sigmoid
        if args['output_fun'] == 'tanh':
            self.output = F.tanh

    def forward(self, x):
        batch_size = x.size(0)
        c = x.view(-1, 1, self.P, self.m)
        c = F.relu(self.conv1(c))
        c = self.dropout(c)
        c = torch.squeeze(c, 3)
        r = c.permute(2, 0, 1).contiguous()
        H_t, r = self.GRU1(r)
        r = self.dropout(torch.squeeze(r, 0))

        if self.model == 'skip':
            s = c[:, :, int(-self.pt * self.skip):].contiguous()
            s = s.view(batch_size, self.hidC, self.pt, self.skip)
            s = s.permute(2, 0, 3, 1).contiguous()
            s = s.view(self.pt, batch_size * self.skip, self.hidC)
            _, s = self.GRUskip(s)
            s = s.view(batch_size, self.skip * self.hidS)
            s = self.dropout(s)
            r = torch.cat((r, s), 1)

        elif self.model == 'attn':
            if self.attn == 'scaled_dot':
                H_t = H_t.permute(1, 0, 2)
                a_w = torch.bmm(H_t, r.unsqueeze(2)) / self.scale
                a_w = torch.softmax(a_w, 1)
                a = torch.bmm(H_t.permute(0, 2, 1), a_w).squeeze(2)
                r = torch.cat((a, r), 1)

            if self.attn == 'cosine':
                H_t = H_t.permute(1, 0, 2)
                r_temp = r.unsqueeze(1).repeat(1, H_t.shape[1], 1)
                a_w = torch.cosine_similarity(H_t, r_temp, 2).unsqueeze(2)
                a_w = torch.softmax(a_w, 1)
                a = torch.bmm(H_t.permute(0, 2, 1), a_w).squeeze(2)
                r = torch.cat((a, r), 1)

            if self.attn == 'multihead':
                a, _ = self.multihead(H_t, H_t, H_t)
                a = a.permute(1, 0, 2)[:, -1, :]
                r = torch.cat((a, r), 1)

        res = self.linear1(r)

        if self.hw > 0:
            z = x[:, -self.hw:, :]
            z = z.permute(0, 2, 1).contiguous().view(-1, self.hw)
            z = self.highway(z)
            z = z.view(-1, self.m)
            res = res + z

        if self.output:
            res = self.output(res)
        return res
