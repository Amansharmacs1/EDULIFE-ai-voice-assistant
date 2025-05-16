import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

# User Interfaces
ax.add_patch(patches.Rectangle((1, 7), 3, 1, fill=True, edgecolor='black', facecolor='#AED6F1'))
ax.text(2.5, 7.5, 'Student UI\n(Login, Submit Experiments)', ha='center', va='center', fontsize=10)

ax.add_patch(patches.Rectangle((6, 7), 3, 1, fill=True, edgecolor='black', facecolor='#AED6F1'))
ax.text(7.5, 7.5, 'Teacher UI\n(Upload, Feedback, Dashboard)', ha='center', va='center', fontsize=10)

# Web Server
ax.add_patch(patches.Rectangle((3.5, 5.5), 3, 1, fill=True, edgecolor='black', facecolor='#F9E79F'))
ax.text(5, 6, 'Web Server\n(Request Handler)', ha='center', va='center', fontsize=10)

# Application Layer
ax.add_patch(patches.Rectangle((1, 4), 3, 1, fill=True, edgecolor='black', facecolor='#A9DFBF'))
ax.text(2.5, 4.5, 'Authentication Service', ha='center', va='center', fontsize=10)

ax.add_patch(patches.Rectangle((4.5, 4), 3, 1, fill=True, edgecolor='black', facecolor='#A9DFBF'))
ax.text(6, 4.5, 'Experiment Mgmt\nService', ha='center', va='center', fontsize=10)

ax.add_patch(patches.Rectangle((8, 4), 3, 1, fill=True, edgecolor='black', facecolor='#A9DFBF'))
ax.text(9.5, 4.5, 'Feedback Service', ha='center', va='center', fontsize=10)

# Database Layer
ax.add_patch(patches.Rectangle((3.5, 2.5), 3, 1, fill=True, edgecolor='black', facecolor='#F5B7B1'))
ax.text(5, 3, 'MongoDB\n(User Data, Experiments, Feedback)', ha='center', va='center', fontsize=10)

# External Services
ax.add_patch(patches.Rectangle((1, 1), 3, 1, fill=True, edgecolor='black', facecolor='#D2B4DE'))
ax.text(2.5, 1.5, 'Email Notification\nService', ha='center', va='center', fontsize=10)

ax.add_patch(patches.Rectangle((6, 1), 3, 1, fill=True, edgecolor='black', facecolor='#D2B4DE'))
ax.text(7.5, 1.5, 'Analytics Service', ha='center', va='center', fontsize=10)

# Arrows
def draw_arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=1.5))

draw_arrow(2.5, 7, 5, 5.5)
draw_arrow(7.5, 7, 5, 5.5)

draw_arrow(5, 5.5, 2.5, 4)
draw_arrow(5, 5.5, 6, 4)
draw_arrow(5, 5.5, 9.5, 4)

draw_arrow(2.5, 4, 5, 2.5)
draw_arrow(6, 4, 5, 2.5)
draw_arrow(9.5, 4, 5, 2.5)

draw_arrow(2.5, 4, 2.5, 2)
draw_arrow(9.5, 4, 7.5, 2)

plt.title('System Architecture Diagram: Lab Sphere - Digital Lab', fontsize=14)
plt.tight_layout()
plt.show()
