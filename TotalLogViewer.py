import numpy as np
import sys
from matplotlib import font_manager
from matplotlib import _pylab_helpers
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import calibration

samplerate = 25.0
  
def main():
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数
    
    # デバッグプリント
    if (argc != 3):   # 引数が足りない場合は、その旨を表示
        print 'Usage: # python %s basedir basename' % argvs[0]
        quit()         # プログラムの終了
        
    calib = calibration.calibration()
    
    #Hページ
    inname = argvs[1] + "\\" + argvs[2] + "_H.csv"
    results_H = np.loadtxt(inname, delimiter=',')
    #Hページの値を処理  
    results_H[:,1] = calib.cranc / results_H[:,1]
    results_H[:,2] = calib.prop / results_H[:,2]
    results_H[:,3] = samplerate * calib.ias1 * results_H[:,3] + calib.ias2
    results_H[:,4] *= calib.alt

    #グラフ描画
    font_path = "C:\Windows\Fonts\meiryo.ttc"
    font_prop = font_manager.FontProperties(fname=font_path)
    font_prop.set_style('normal')
    font_prop.set_weight('light')
    font_prop.set_size('large')
    
    figsize = (24, 13.5)
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(hspace=0.001)
    ax1 = fig.add_subplot(111)
    ax1r = ax1.twinx()
    line1 = ax1.plot(results_H[:,0], results_H[:,1], color = 'r', label = u"クランク回転数")
    line2 = ax1.plot(results_H[:,0], results_H[:,2] * 0.5, color = 'g', label = u"プロペラ回転数")
    line3 = ax1r.plot(results_H[:,0], results_H[:,3], color = 'b', label = u"対気速度")
    line4 = ax1r.plot(results_H[:,0], results_H[:,4], color = 'k', label = u"対地高度")
    ax1.set_yticks(np.arange(0.0, 150.1, 50.0))
    ax1.set_ylim(0.0,150.0)
    ax1r.set_yticks(np.arange(0.0, 15.1, 5.0))
    ax1r.set_ylim(0.0,15.0)
    formatter = ticker.FormatStrFormatter('%0.0f')
    ax1.xaxis.set_major_formatter(formatter)
    ax1.set_title(argvs[1] + "\\" + argvs[2], fontproperties=font_prop)
    ax1.set_xlabel(u"GPS時刻[s]", fontproperties=font_prop)
    ax1.set_ylabel(u"クランク回転数[rpm]\nプロペラ回転数[x0.5rpm]", fontproperties=font_prop)
    ax1r.set_ylabel(u"対気速度[m/s]\n対地高度[m]", fontproperties=font_prop)
    ax1.grid(True)
    ax1.legend(prop=font_prop, bbox_to_anchor=(0.885, 1.0), loc=2, borderaxespad=0., frameon = False)
    ax1r.legend(prop=font_prop, bbox_to_anchor=(0.885, 0.935), loc=2, borderaxespad=0., frameon = False)
    
    canvas = FigureCanvasAgg(fig)  
       
    plt.figure(1, figsize=figsize)
    figManager = _pylab_helpers.Gcf.get_active()
    figManager.canvas.figure = fig
    plt.show()

if __name__ == '__main__':
    main()