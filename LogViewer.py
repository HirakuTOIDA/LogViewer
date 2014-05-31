import numpy as np
import sys
import math
from scipy.interpolate import interp1d
import pylab as pl
from matplotlib import font_manager
from matplotlib import _pylab_helpers
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import calibration

#リサンプルのレート設定
samplerate = 25.0

# ヨー角の不連続補正
# 0: -180 - 180 deg.
# 1: 0 - 360 deg.
modifyyaw = 1

# 各種オフセット補正
pitch_offset = 0.0
roll_offset = 0.0
yaw_offset = 0.0
rudder_offset = 0.0
elevetor_offset = 0.0
aileron_offset = 0.0

# 使うログファイルの設定
hpanavi = 0
tinyfeather = 0

def read_page(d, computed_time, page):
    if page == "A":
        row_time = 1
        row_min = 2
        row_max = 11
    elif page == "M":
        row_time = 0
        row_min = 2
        row_max = 5
    elif page == "H":
        row_time = 0
        row_min = 1
        row_max = 13
    else:
        row_time = 0
        row_min = 1
        row_max = 10
    linear_results=[]   #リストの初期化
    linear_results.append(computed_time)
    for i in range(row_min, row_max):
        linear_interp = interp1d(d[:,row_time], d[:,i])    #直線補間
        linear_results.append(linear_interp(computed_time))
    return linear_results
    
def main():
    argvs = sys.argv  # コマンドライン引数を格納したリストの取得
    argc = len(argvs) # 引数の個数
    
    # デバッグプリント
    if (argc != 3):   # 引数が足りない場合は、その旨を表示
        print 'Usage: # python %s basedir basename' % argvs[0]
        quit()         # プログラムの終了
        
    calib = calibration.calibration()
    
    if (hpanavi == 1 and tinyfeather == 1):
        basedir1 = argvs[1] + "\\HPANavi\\"
        basedir2 = argvs[1] + "\\TinyFeather\\"
    elif (hpanavi == 1 and tinyfeather == 0):
        basedir1 = argvs[1] + "\\HPANavi\\"
        basedir2 = argvs[1] + "\\HPANavi\\"
    else:        
        basedir1 = argvs[1] + "\\"
        basedir2 = argvs[1] + "\\"
        
    #Gページ    
    inname = basedir2 + argvs[2] + "_G.csv"
    outname = basedir2 + argvs[2] + "_G_out.csv"
    d = np.loadtxt(inname, delimiter=',')
    #GPS時刻を基準にする。ログの切り出し誤差を考慮して最初と最後の1秒ずつは捨てる
    computed_time = np.linspace(d[0,0] + 1.0, d[-1,0] - 1.0, (d[-1,0] - 1.0 - d[0,0] - 1.0) * samplerate + 1)
    results_G = read_page(d, computed_time, "G")
    GS=[]
    for i in range(len(results_G[6])):
        GS.append(math.sqrt(results_G[6][i]*results_G[6][i]+results_G[7][i]*results_G[7][i]))
    np.savetxt(outname, zip(*results_G), delimiter=',') 

    #Aページ 
    inname = basedir2 + argvs[2] + "_A.csv"
    outname = basedir2 + argvs[2] + "_A_out.csv"
    d = np.loadtxt(inname, delimiter=',')
    results_A = read_page(d, computed_time, "A")
    np.savetxt(outname, zip(*results_A), delimiter=',')
    
    #Mページ
    inname = basedir2 + argvs[2] + "_M.csv"
    outname = basedir2 + argvs[2] + "_M_out.csv"
    d = np.loadtxt(inname, delimiter=',') 
    d[:,0] += ( d[:,1] * 0.04)  #indexを処理
    results_M = read_page(d, computed_time, "M")
    np.savetxt(outname, zip(*results_M), delimiter=',')
    
    #Hページ
    inname = basedir1 + argvs[2] + "_H.csv"
    outname = basedir1 + argvs[2] + "_H_out.csv"
    d = np.loadtxt(inname, delimiter=',') 
    results_H = read_page(d, computed_time, "H")
    #Hページの値を処理  
    results_H[1] = calib.cranc / results_H[1]
    results_H[2] = calib.prop / results_H[2]
    results_H[3] = samplerate * calib.ias1 * results_H[3] + calib.ias2
    results_H[4] *= calib.alt
    results_H[5] = (results_H[5] - calib.aileron2) / calib.adcmax * calib.encordermax * calib.aileron1
    results_H[6] = -(results_H[6] - calib.rudder2) / calib.adcmax * calib.encordermax * calib.rudder1
    results_H[7] = (results_H[7] - calib.elevetor2) / calib.adcmax * calib.encordermax * calib.elevetor1
    np.savetxt(outname, zip(*results_H), delimiter=',')

    #Nページ
    inname = basedir2 + argvs[2] + "_N.csv"
    outname = basedir2 + argvs[2] + "_N_out.csv"    
    d = np.loadtxt(inname, delimiter=',')
    if modifyyaw == 1:
        for i in range(len(d[:,7])):
            if d[i,7] < 0:
                d[i,7] += 360.0
    results_N = read_page(d, computed_time, "N")
    np.savetxt(outname, zip(*results_N), delimiter=',')

    #グラフ描画
    font_path = "C:\Windows\Fonts\meiryo.ttc"
    font_prop = font_manager.FontProperties(fname=font_path)
    font_prop.set_style('normal')
    font_prop.set_weight('light')
    font_prop.set_size('large')
    
    figsize = (24, 13.5)
    fig = plt.figure(figsize=figsize)
    fig.subplots_adjust(hspace=0.001)

    ax1 = fig.add_subplot(311)
    ax1r = ax1.twinx()
    line1 = ax1.plot(results_H[0], results_H[1], color = 'r', label = u"クランク回転数")
    line2 = ax1.plot(results_H[0], results_H[2] * 0.5, color = 'g', label = u"プロペラ回転数")
    line3 = ax1r.plot(results_H[0], results_H[3], color = 'b', label = u"対気速度")
    line4 = ax1r.plot(results_G[0], GS, color = 'c', label = u"対地速度")
    line5 = ax1r.plot(results_H[0], results_H[4], color = 'k', label = u"対地高度")
    ax1.set_yticks(pl.arange(0.0, 150.1, 50.0))
    ax1.set_ylim(0.0,150.0)
    ax1r.set_yticks(pl.arange(0.0, 15.1, 5.0))
    ax1r.set_ylim(0.0,15.0)
    ax1.set_title(argvs[1] + "\\" + argvs[2], fontproperties=font_prop)
    ax1.set_xlabel('')
    ax1.set_ylabel(u"クランク回転数[rpm]\nプロペラ回転数[x0.5rpm]", fontproperties=font_prop)
    ax1r.set_ylabel(u"対気速度[m/s]\n対地高度[m]", fontproperties=font_prop)
    ax1.set_xticklabels('', False)
    ax1.grid(True)
    ax1.legend(prop=font_prop, bbox_to_anchor=(0.885, 1.0), loc=2, borderaxespad=0., frameon = False)
    ax1r.legend(prop=font_prop, bbox_to_anchor=(0.885, 0.815), loc=2, borderaxespad=0., frameon = False)
    
    ax2 = fig.add_subplot(312)    
    ax2r = ax2.twinx()
    if hpanavi == 0:
        line6 = ax2.plot(results_N[0], results_N[8] + pitch_offset, color = 'r', label = u"ピッチ角")
        line7 = ax2.plot(results_N[0], results_N[9] + roll_offset, color = 'b', label = u"ロール角")
    else:
        line6 = ax2.plot(results_N[0], results_N[9] + pitch_offset, color = 'r', label = u"ピッチ角") 
        line7 = ax2.plot(results_N[0], results_N[8] + roll_offset, color = 'b', label = u"ロール角")       
    line5 = ax2r.plot(results_N[0], results_N[7] + yaw_offset, color = 'g', label = u"ヨー角")
    ax2.set_yticks(pl.arange(-25.0, 25.0, 5.0))
    ax2.set_ylim(-25.0,25.0)
    ax2.set_xlabel('')
    ax2.set_ylabel(u"ピッチ角[deg.]\nロール角[deg.]", fontproperties=font_prop)
    ax2r.set_ylabel(u"ヨー角[deg.]", fontproperties=font_prop)
    ax2.set_xticklabels('', False)
    ax2.grid(True) 
    ax2.legend(prop=font_prop, bbox_to_anchor=(0.885, 1.0), loc=2, borderaxespad=0., frameon = False)
    ax2r.legend(prop=font_prop, bbox_to_anchor=(0.885, 0.815), loc=2, borderaxespad=0., frameon = False)
    
    ax3 = fig.add_subplot(313)    
    line10 = ax3.plot(results_H[0], results_H[7] + elevetor_offset, color = 'r', label = u"エレベータ舵角")
    line8 = ax3.plot(results_H[0], results_H[5] + aileron_offset, color = 'b', label = u"エルロン舵角")
    line9 = ax3.plot(results_H[0], results_H[6] + rudder_offset, color = 'g', label = u"ラダー舵角")
    ax3.set_yticks(pl.arange(-25.0, 25.0, 5.0))
    ax3.set_ylim(-25.0, 25.0)
    ax3.set_xlabel(u"GPS時刻[s]", fontproperties=font_prop)
    ax3.set_ylabel(u"エレベータ舵角[deg.]\nエルロン舵角[deg.]\nラダー舵角[deg.]", fontproperties=font_prop)
    ax3.grid(True)
    ax3.legend(prop=font_prop, bbox_to_anchor=(0.885, 1.0), loc=2, borderaxespad=0., frameon = False)
    
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(argvs[1] + "\\" + argvs[2] + "_out.png", dpi=80)
       
    pl.figure(1, figsize=figsize)
    figManager = _pylab_helpers.Gcf.get_active()
    figManager.canvas.figure = fig
    pl.show()

if __name__ == '__main__':
    main()