import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. الدالة الرياضية لحساب مساحة تقاطع قرصين (Overlapping Circles)
# ============================================================
def circle_overlap(d, R1, R2):
    """
    حساب مساحة الجزء المتقاطع بين قرصين المسافة بين مركزيهما d ونصف قطريهما R1 و R2.
    """
    if d >= R1 + R2:
        return 0.0  # لا يوجد تقاطع
    if d <= abs(R1 - R2):
        return np.pi * min(R1, R2)**2  # كسوف كلي أو حلقي
    
    # حساب أجزاء المساحة باستخدام هندسة القطاعات الدائرية
    r1_sq = R1**2
    r2_sq = R2**2
    
    part1 = r1_sq * np.arccos((d**2 + r1_sq - r2_sq) / (2 * d * R1))
    part2 = r2_sq * np.arccos((d**2 + r2_sq - r1_sq) / (2 * d * R2))
    part3 = 0.5 * np.sqrt((-d + R1 + R2) * (d + R1 - R2) * (d - R1 + R2) * (d + R1 + R2))
    
    return part1 + part2 - part3

# ============================================================
# 2. إعدادات النظام الثنائي (Physical Parameters)
# ============================================================
P = 1.0          # الدورة المدارية (أيام)
R1 = 0.2         # نصف قطر النجم الرئيسي (بالوحدات النسبية للمدار)
R2 = 0.12        # نصف قطر النجم الثانوي
L1 = 0.8         # لمعان النجم الرئيسي
L2 = 0.2         # لمعان النجم الثانوي
I_surface1 = L1 / (np.pi * R1**2) # شدة الإضاءة السطحية للنجم 1
I_surface2 = L2 / (np.pi * R2**2) # شدة الإضاءة السطحية للنجم 2

# ============================================================
# 3. محاكاة الحركة المدارية (Simulation)
# ============================================================
time = np.linspace(0, P, 1000)
phase = time / P
theta = 2 * np.pi * phase

# حساب الإحداثيات (x, y) للنجمين في المدار (مدار دائري)
# نفترض أننا نرى النظام من الحافة (Inclination = 90)
x1 = 0.5 * np.cos(theta)
y1 = 0.5 * np.sin(theta)
x2 = -0.5 * np.cos(theta)
y2 = -0.5 * np.sin(theta)

# المسافة المسقطة في مستوى السماء (Z-plane is toward us)
# الكسوف يحدث عندما يقترب x1 من x2 في الإسقاط
d_projected = np.abs(x1 - x2)

flux_list = []

for i in range(len(time)):
    total_flux = L1 + L2
    
    # التحقق من وجود كسوف
    if d_projected[i] < (R1 + R2):
        overlap_area = circle_overlap(d_projected[i], R1, R2)
        
        # الكسوف الرئيسي (النجم 2 أمام النجم 1) - يحدث عند طور 0.5
        if y2[i] > y1[i]:
            total_flux -= overlap_area * I_surface1
        # الكسوف الثانوي (النجم 1 أمام النجم 2) - يحدث عند طور 0.0 أو 1.0
        else:
            total_flux -= overlap_area * I_surface2
            
    flux_list.append(total_flux)

# تحويل اللمعان إلى أقدار ظاهرية (Magnitude) باستخدام معادلة بوغسون
mag = -2.5 * np.log10(np.array(flux_list))

# حفظ البيانات في DataFrame
df = pd.DataFrame({
    'Phase': phase,
    'Flux': flux_list,
    'Magnitude': mag
})

# ============================================================
# 4. الرسم البياني (Visualization)
# ============================================================
plt.figure(figsize=(10, 6))
plt.plot(df['Phase'], df['Magnitude'], color='black', linewidth=2)

# التقاليد الفلكية: قلب محور الصادات (الأرقام الصغيرة في الأعلى تعني أسطع)
plt.gca().invert_yaxis()

plt.title('Simulated Eclipsing Binary Light Curve', fontsize=14)
plt.xlabel('Orbital Phase', fontsize=12)
plt.ylabel('Relative Magnitude', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# تحديد مناطق الكسوف
plt.text(0.5, df['Magnitude'].max() + 0.02, 'Primary Eclipse', ha='center', color='red')
plt.text(0.0, df['Magnitude'].min() + 0.02, 'Secondary', ha='center', color='blue')
plt.text(1.0, df['Magnitude'].min() + 0.02, 'Secondary', ha='center', color='blue')

plt.tight_layout()
plt.savefig('light_curve_simulation.png', dpi=300)
plt.show()

print("--- تم الانتهاء من المحاكاة وحفظ الرسم البياني ---")
