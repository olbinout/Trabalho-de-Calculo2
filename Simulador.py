import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Parâmetros iniciais
R = 18  
Area_Total = np.pi * R**2

# Configuração da figura e do gráfico
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(bottom=0.25) 
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect('equal') 
ax.set_title('Simulador de Divisão da Pizza (Cortes Paralelos)', fontsize=14)
ax.axis('off') 

# Coordenadas X e as curvas superior e inferior do círculo
x = np.linspace(-R, R, 1000)
y_upper = np.sqrt(R**2 - x**2)
y_lower = -y_upper

# Desenhando a borda da pizza
circle = plt.Circle((0, 0), R, color='#D2691E', fill=False, linewidth=4)
ax.add_patch(circle)

# Elementos visuais que serão atualizados
line_left = ax.axvline(0, color='red', linestyle='--', linewidth=2)
line_right = ax.axvline(0, color='red', linestyle='--', linewidth=2)

text_left = ax.text(-11, 0, '', ha='center', va='center', fontsize=14, color='white', weight='bold', bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
text_center = ax.text(0, 0, '', ha='center', va='center', fontsize=14, color='white', weight='bold', bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
text_right = ax.text(11, 0, '', ha='center', va='center', fontsize=14, color='white', weight='bold', bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

# Criando o eixo do Slider
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgray')
slider_a = Slider(
    ax=ax_slider,
    label='Distância do Corte (a)',
    valmin=0.0,
    valmax=18.0,
    valinit=4.766, 
    valfmt='%0.2f cm'
)

# Função para atualizar o gráfico conforme o slider se move
def update(val):
    a = slider_a.val
    
    # Limpa os preenchimentos anteriores (as fatias coloridas)
    ax.collections.clear()
    
    # Redesenha as fatias coloridas com base no novo valor de 'a'
    ax.fill_between(x[x <= -a], y_upper[x <= -a], y_lower[x <= -a], color='#FF6347', alpha=0.8) # Esquerda
    ax.fill_between(x[(x >= -a) & (x <= a)], y_upper[(x >= -a) & (x <= a)], y_lower[(x >= -a) & (x <= a)], color='#FFD700', alpha=0.6) # Centro
    ax.fill_between(x[x >= a], y_upper[x >= a], y_lower[x >= a], color='#FF6347', alpha=0.8) # Direita
    
    # Atualiza a posição das linhas de corte
    line_left.set_xdata([-a, -a])
    line_right.set_xdata([a, a])
    
    # Cálculo das áreas usando as fórmulas geométricas de segmento circular
    if a < R:
        area_borda = (R**2 * np.arccos(a/R)) - (a * np.sqrt(R**2 - a**2))
    else:
        area_borda = 0
        
    area_centro = Area_Total - (2 * area_borda)
    
    # Cálculo das porcentagens
    pct_borda = (area_borda / Area_Total) * 100
    pct_centro = (area_centro / Area_Total) * 100
    
    # Atualiza os textos
    text_left.set_text(f'{pct_borda:.1f}%')
    text_center.set_text(f'{pct_centro:.1f}%')
    text_right.set_text(f'{pct_borda:.1f}%')
    
    # Destaque visual se a divisão estiver muito próxima de 1/3 para todos (33.3%)
    if abs(pct_borda - 33.33) < 0.5:
        text_left.set_color('#32CD32')  # Fica verde ao acertar
        text_center.set_color('#32CD32')
        text_right.set_color('#32CD32')
    else:
        text_left.set_color('white')
        text_center.set_color('white')
        text_right.set_color('white')
        
    fig.canvas.draw_idle()

# Conecta o slider à função de atualização e inicializa
slider_a.on_changed(update)
update(slider_a.val)

# Mostra a janela interativa
plt.show()