#!/usr/bin/env python3
"""
Neo-Noir Tactical HUD Dashboard Visualizer
Inspired by Batcomputer and JARVIS - Red-on-black holographic tactical interface
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Wedge, Rectangle
import numpy as np
from datetime import datetime
import os

# Neo-noir color scheme
COLORS = {
    'background': '#000000',
    'primary_red': '#FF0040',
    'alert_red': '#FF1744',
    'glow_red': '#FF5252',
    'dark_red': '#8B0000',
    'accent_white': '#FFFFFF',
    'grid_gray': '#1A1A1A',
    'text_glow': '#FF6B6B',
    'hologram_blue': '#00D4FF',
    'warning_orange': '#FF6600'
}

class TacticalHUD:
    def __init__(self):
        self.fig = plt.figure(figsize=(16, 12), facecolor=COLORS['background'])
        self.ax = self.fig.add_subplot(111, facecolor=COLORS['background'])
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.axis('off')
        
    def load_system_data(self):
        """Load data from AAI system files"""
        data = {
            'phase': 'Enhancement Phase',
            'phase_progress': 100,  # Core phases complete
            'enhancement_progress': 40,
            'cache': 35,
            'states': 25,
            'queue': 80,
            'archives': 60,
            'active_tasks': 13,
            'conflicts': 0,
            'system_health': 'OPTIMAL',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')
        }
        
        # Try to load real data
        try:
            with open('/mnt/c/Users/Brandon/AAI/brain/logs/queue.json', 'r') as f:
                queue_data = json.load(f)
                data['active_tasks'] = queue_data['metadata']['active_items']
                data['queue'] = int((data['active_tasks'] / 20) * 100)  # Assuming 20 max tasks
        except:
            pass
            
        return data
    
    def draw_holographic_grid(self):
        """Draw background holographic grid"""
        for i in range(-10, 11, 2):
            self.ax.axhline(y=i, color=COLORS['grid_gray'], alpha=0.3, linewidth=0.5)
            self.ax.axvline(x=i, color=COLORS['grid_gray'], alpha=0.3, linewidth=0.5)
            
    def draw_central_core(self, data):
        """Draw the central AI core with pulsing effect"""
        # Outer glow
        for i in range(5, 0, -1):
            circle = Circle((0, 0), 1.5 + i*0.2, 
                          facecolor='none', 
                          edgecolor=COLORS['primary_red'], 
                          alpha=0.1*i, 
                          linewidth=2)
            self.ax.add_patch(circle)
        
        # Core circle
        core = Circle((0, 0), 1.5, 
                     facecolor=COLORS['background'], 
                     edgecolor=COLORS['primary_red'], 
                     linewidth=3)
        self.ax.add_patch(core)
        
        # Core text
        self.ax.text(0, 0.3, 'AAI v3.0', 
                    fontsize=16, 
                    color=COLORS['accent_white'], 
                    ha='center', 
                    weight='bold',
                    family='monospace')
        self.ax.text(0, -0.3, 'TACTICAL MODE', 
                    fontsize=10, 
                    color=COLORS['primary_red'], 
                    ha='center',
                    family='monospace')
        
    def draw_phase_ring(self, data):
        """Draw phase progress ring with segments"""
        # Phase segments
        phases = [
            ('FOUNDATION', 100, COLORS['dark_red']),
            ('INTELLIGENCE', 100, COLORS['dark_red']),
            ('OPTIMIZATION', 100, COLORS['dark_red']),
            ('ENHANCEMENT', data['enhancement_progress'], COLORS['primary_red'])
        ]
        
        angle_per_phase = 360 / len(phases)
        
        for i, (name, progress, color) in enumerate(phases):
            start_angle = i * angle_per_phase
            # Background segment
            bg_wedge = Wedge((0, 0), 3, start_angle, start_angle + angle_per_phase,
                           width=0.5, facecolor=COLORS['grid_gray'], alpha=0.5)
            self.ax.add_patch(bg_wedge)
            
            # Progress segment
            progress_angle = (progress / 100) * angle_per_phase
            if progress > 0:
                wedge = Wedge((0, 0), 3, start_angle, start_angle + progress_angle,
                            width=0.5, facecolor=color, alpha=0.8)
                self.ax.add_patch(wedge)
                
    def draw_memory_ring(self, data):
        """Draw memory utilization ring"""
        metrics = [
            ('CACHE', data['cache'], 0),
            ('STATES', data['states'], 90),
            ('QUEUE', data['queue'], 180),
            ('ARCHIVE', data['archives'], 270)
        ]
        
        for name, value, start_angle in metrics:
            # Background arc
            bg_wedge = Wedge((0, 0), 4.5, start_angle, start_angle + 90,
                           width=0.8, facecolor=COLORS['grid_gray'], alpha=0.3)
            self.ax.add_patch(bg_wedge)
            
            # Value arc
            value_angle = (value / 100) * 90
            color = COLORS['primary_red'] if value < 80 else COLORS['warning_orange']
            wedge = Wedge((0, 0), 4.5, start_angle, start_angle + value_angle,
                        width=0.8, facecolor=color, alpha=0.7)
            self.ax.add_patch(wedge)
            
            # Label
            label_angle = np.radians(start_angle + 45)
            x = 5.5 * np.cos(label_angle)
            y = 5.5 * np.sin(label_angle)
            self.ax.text(x, y, f'{name}\n{value}%', 
                        fontsize=9, 
                        color=COLORS['text_glow'],
                        ha='center', 
                        va='center',
                        family='monospace')
            
    def draw_alert_ring(self, data):
        """Draw alert/conflict monitoring ring"""
        # Alert indicators
        alerts = [
            ('TASKS', data['active_tasks'], 0, COLORS['primary_red']),
            ('CONFLICTS', data['conflicts'], 120, COLORS['hologram_blue']),
            ('ALERTS', 0, 240, COLORS['warning_orange'])
        ]
        
        for name, count, angle, color in alerts:
            rad = np.radians(angle)
            x = 6.5 * np.cos(rad)
            y = 6.5 * np.sin(rad)
            
            # Alert box
            box = Rectangle((x-1, y-0.5), 2, 1, 
                          facecolor=COLORS['background'],
                          edgecolor=color,
                          linewidth=2)
            self.ax.add_patch(box)
            
            # Alert text
            self.ax.text(x, y, f'{count}', 
                        fontsize=14, 
                        color=color,
                        ha='center', 
                        va='center',
                        weight='bold',
                        family='monospace')
            self.ax.text(x, y-0.8, name, 
                        fontsize=8, 
                        color=color,
                        ha='center',
                        family='monospace')
            
    def draw_waveform_display(self, data):
        """Draw system vitals waveform"""
        x = np.linspace(-8, -3, 100)
        y = np.sin(x * 2) * 0.3 + 7
        
        # Glow effect
        for i in range(3):
            self.ax.plot(x, y, color=COLORS['primary_red'], alpha=0.3-i*0.1, linewidth=3-i)
        
        self.ax.text(-5.5, 8, 'SYSTEM VITALS', 
                    fontsize=10, 
                    color=COLORS['primary_red'],
                    ha='center',
                    family='monospace')
        self.ax.text(-5.5, 6.2, data['system_health'], 
                    fontsize=12, 
                    color=COLORS['accent_white'],
                    ha='center',
                    weight='bold',
                    family='monospace')
        
    def draw_mission_timer(self, data):
        """Draw mission-critical timer display"""
        # Timer box
        timer_box = Rectangle((2, 6), 6, 2.5, 
                            facecolor=COLORS['background'],
                            edgecolor=COLORS['primary_red'],
                            linewidth=2)
        self.ax.add_patch(timer_box)
        
        # Timer text
        self.ax.text(5, 7.5, 'NEXT PHASE', 
                    fontsize=10, 
                    color=COLORS['primary_red'],
                    ha='center',
                    family='monospace')
        self.ax.text(5, 6.8, '< 24:00:00 >', 
                    fontsize=14, 
                    color=COLORS['accent_white'],
                    ha='center',
                    weight='bold',
                    family='monospace')
        
    def draw_header(self, data):
        """Draw header with timestamp"""
        self.ax.text(0, 9.5, 'TACTICAL OPERATIONS DASHBOARD', 
                    fontsize=20, 
                    color=COLORS['primary_red'],
                    ha='center',
                    weight='bold',
                    family='monospace')
        self.ax.text(0, 8.8, data['timestamp'], 
                    fontsize=10, 
                    color=COLORS['text_glow'],
                    ha='center',
                    family='monospace')
        
    def generate_dashboard(self):
        """Generate the complete dashboard"""
        data = self.load_system_data()
        
        self.draw_holographic_grid()
        self.draw_central_core(data)
        self.draw_phase_ring(data)
        self.draw_memory_ring(data)
        self.draw_alert_ring(data)
        self.draw_waveform_display(data)
        self.draw_mission_timer(data)
        self.draw_header(data)
        
        # Save the figure
        output_path = '/mnt/c/Users/Brandon/AAI/brain/logs/dashboards/tactical-hud.png'
        self.fig.savefig(output_path, 
                        facecolor=COLORS['background'], 
                        dpi=150, 
                        bbox_inches='tight',
                        pad_inches=0.5)
        plt.close()
        
        return output_path

if __name__ == '__main__':
    hud = TacticalHUD()
    output = hud.generate_dashboard()
    print(f"Dashboard generated: {output}")