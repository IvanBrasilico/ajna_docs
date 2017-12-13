import imageio

def find_conteiner(afile):
    """Heuristic dumb walk algorithm
    Beginning on middle of top, left, right and bottom sizes,
    do a 'walk till find wall(gray>230)'.
    Besides simplicity, works well to find conteiner boundaries on majority of cases,
    so is a beggining and can acelerate anottations for training better algorithm
    
    Args:
    
    afile: caminho da imagem no disco
    
    Returns:
    
    xleft, ytop, xright, ybottom
    
    """
    im = imageio.imread(afile)[:,:,0]
    yfinal, xfinal = im.shape
    ymeio = round(yfinal / 2)
    xmeio = round(xfinal / 2)
    #primeiro achar o Teto do contêiner. Tentar primeiro exatamente no meio
    yteto = 0
    for s in range(0, ymeio):
        if (im[s, xmeio] < 230):
            yteto = s
            break
    #Depois de achado o teto, percorrer as laterais para achar os lados
    xesquerda = 1
    for r in range(0, xmeio):
        if (im[yteto+5, r] < 230):
            xesquerda = r
            break
    xdireita = xfinal - 1
    for r in range(xfinal-1, xmeio, -1):
        if (im[yteto+5, r] < 215):
            xdireita = r
            break
    #Achar o piso do contêiner é bem mais difícil... Pensar em como fazer depois Talvez o ponto de max valores
    imbaixo = im[ymeio:yfinal, xesquerda:xdireita]
    ychao = imbaixo.sum(axis=1).argmin()
    ychao = ychao + ymeio + 10
    #Por fim, fazer umas correções se as medidas achadas forem absurdas
    if (ychao>yfinal):
        ychao = yfinal
    if ((xdireita-xesquerda) < (xfinal/4)):
        xdireita = xfinal - 5
        xesquerda = 5
    if (yteto == ymeio):
        yteto = 5
    return xesquerda, yteto, xdireita, ychao
