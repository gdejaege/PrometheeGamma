from matplotlib import pyplot as plt

class OrthogonalGraph:
    def __init__(self, gamma_matrix:list, matrix_results:list, Ti:float, Tj:float) -> None:
        self.x = []
        self.y = []
        xb = []
        xv = []
        xr = []
        yb = []
        yv = []
        yr = []
        
        for i in range(len(gamma_matrix)):
            for j in range(len(gamma_matrix[i])):
                self.x.append(gamma_matrix[i][j])
                self.y.append(gamma_matrix[j][i])

        
        for k in range(len(self.x)):
            if(self.x[k]<=Ti and self.y[k]<=Ti):
                xv.append(self.x[k])
                yv.append(self.y[k])
            elif(self.x[k]>=Tj and self.y[k]>=Tj):
                xr.append(self.x[k])
                yr.append(self.y[k])
            else:
                xb.append(self.x[k])
                yb.append(self.y[k])
        

        plt.figure('Orthogonal graph')
        #plt.plot(self.x, self.y, 'bo')
        plt.plot(xv, yv, 'go')
        plt.plot(xr, yr, 'ro')
        plt.plot(xb, yb, 'bo')
        plt.xlabel('γij')
        plt.ylabel('γji')

    def show(self):
        plt.show()