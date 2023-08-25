import c3d



reader = c3d.Reader(open('D:/1.c3d', 'rb'))
for i, points, analog in reader.read_frames():
    print('frame {}: point {}, analog {}'.format(i, points.shape, analog.shape))