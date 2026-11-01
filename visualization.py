from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import random
import numpy as np

def visualizationpreprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result):
    def mapped(value, options):
        return options[str(value).strip().lower()]

    cp = mapped(cp, {"typical angina": 0, "atypical angina": 1, "non-anginal pain": 2, "asymptomatic": 3})
    fbs = mapped(fbs, {"yes": 1, "no": 0})
    restecg = mapped(restecg, {"nothing to note": 0, "st-t wave abnormality": 1, "possible or definite left ventricular hypertrophy": 2})
    exang = mapped(exang, {"yes": 1, "no": 0})
    slope = mapped(slope, {"upsloping: better heart rate with excercise(uncommon)": 0, "flatsloping: minimal change(typical healthy heart)": 1, "downsloping: signs of unhealthy heart": 2})
    thal = mapped(thal, {"fixed defect: used to be defect but ok now": 6, "reversable defect: no proper blood movement when excercising": 7, "normal": 3})
    
    #final_list=[int(cp),int(trestbps),int(restecg),int(chol),int(fbs),int(thalach),int(exang),float(oldpeak),int(slope),int(ca),int(thal)]
    normal_value1=[0.478261,0.159420,0.449275,0.550725,1.585507,1.166667,1.166667,2.543478]
    user_value1=[float(cp),float(fbs),float(restecg),float(exang),float(oldpeak),float(slope),float(ca),float(thal)]
    normal_value2=[134.398551,251.086957,139.101449]
    user_value2=[float(trestbps),float(chol),float(thalach)]
    list1=[normal_value1,user_value1]
    list2=[normal_value2,user_value2]

    return list1,list2

# def create_figure1(data1):
#     fig = plt.figure()
#     axis = fig.add_axes([0,0,1,1])
#     y1 = data1[0]
#     y2 = data1[1]
#     width = 0.30
#     x=np.arange(8)
#     axis.bar(x-0.3, y1, width, color='cyan')
#     axis.bar(x, y2, width, color='orange')
#     # axis.bar(xs, ys)
#     # axis.xticks(x, ['cp','chol','fbs','exang','oldpeak','slope','ca','thal'])
#     # axis.xlabel("Heart health defining attributes")
#     axis.set_ylabel("values")
#     # axis.legend(["Normal", "Yours"])
#     axis.set_title('Your data corresponding to normal data')
#     return fig




