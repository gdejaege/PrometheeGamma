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
                #self.x.append(gamma_matrix[i][j])
                #self.y.append(gamma_matrix[j][i])
                if(len(matrix_results[i][j].split('P')) > 1):
                    xb.append(gamma_matrix[i][j])
                    yb.append(gamma_matrix[j][i])
                elif(len(matrix_results[i][j].split('I')) > 1):
                    xv.append(gamma_matrix[i][j])
                    yv.append(gamma_matrix[j][i])
                elif(len(matrix_results[i][j].split('J')) > 1):
                    xr.append(gamma_matrix[i][j])
                    yr.append(gamma_matrix[j][i])

        """
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
        """
        
        plt.figure('Orthogonal graph')
        #plt.plot(self.x, self.y, 'bo')
        plt.plot(xv, yv, 'go',markersize=2)
        plt.plot(xr, yr, 'ro',markersize=2)
        plt.plot(xb, yb, 'bo',markersize=2)
        plt.xlabel('γij')
        plt.ylabel('γji')

    def show(self):
        plt.show()