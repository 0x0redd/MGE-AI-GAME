import pygame
import random
import math
from scripts.brand_config import *

class CircuitPattern:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_size = CIRCUIT_GRID_SIZE
        self.nodes = []
        self.connections = []
        self.animation_time = 0
        self.glow_intensity = 0
        
        self.generate_circuit()
    
    def generate_circuit(self):
        """Generate a circuit board pattern with nodes and connections"""
        # Create grid of potential nodes
        cols = self.width // self.grid_size
        rows = self.height // self.grid_size
        
        # Generate nodes with some randomness
        for col in range(cols + 1):
            for row in range(rows + 1):
                if random.random() < CIRCUIT_DENSITY:
                    x = col * self.grid_size + random.randint(-10, 10)
                    y = row * self.grid_size + random.randint(-10, 10)
                    node = {
                        'pos': (x, y),
                        'active': random.random() < 0.3,
                        'pulse_phase': random.uniform(0, 2 * math.pi),
                        'connections': []
                    }
                    self.nodes.append(node)
        
        # Create connections between nearby nodes
        for i, node1 in enumerate(self.nodes):
            for j, node2 in enumerate(self.nodes[i+1:], i+1):
                distance = math.sqrt((node1['pos'][0] - node2['pos'][0])**2 + 
                                   (node1['pos'][1] - node2['pos'][1])**2)
                if distance < self.grid_size * 1.5 and random.random() < CIRCUIT_CONNECTION_PROBABILITY:
                    connection = {
                        'start': node1['pos'],
                        'end': node2['pos'],
                        'active': node1['active'] or node2['active'],
                        'pulse_phase': random.uniform(0, 2 * math.pi)
                    }
                    self.connections.append(connection)
                    node1['connections'].append(j)
                    node2['connections'].append(i)
    
    def update(self, dt):
        """Update circuit animation"""
        self.animation_time += dt * ANIMATION_SPEED
        self.glow_intensity = 0.5 + 0.5 * math.sin(self.animation_time * GLOW_PULSE_SPEED)
        
        # Update node pulses
        for node in self.nodes:
            node['pulse_phase'] += dt * 2
            if node['pulse_phase'] > 2 * math.pi:
                node['pulse_phase'] -= 2 * math.pi
        
        # Update connection pulses
        for connection in self.connections:
            connection['pulse_phase'] += dt * 1.5
            if connection['pulse_phase'] > 2 * math.pi:
                connection['pulse_phase'] -= 2 * math.pi
    
    def draw(self, surface, offset=(0, 0)):
        """Draw the circuit pattern"""
        # Draw connections first (behind nodes)
        for connection in self.connections:
            start_pos = (connection['start'][0] + offset[0], connection['start'][1] + offset[1])
            end_pos = (connection['end'][0] + offset[0], connection['end'][1] + offset[1])
            
            # Calculate pulse effect
            pulse = 0.5 + 0.5 * math.sin(connection['pulse_phase'])
            alpha = int(100 + 155 * pulse * self.glow_intensity)
            
            # Create color with alpha - ensure proper RGBA format
            color = (int(CIRCUIT_LINE[0]), int(CIRCUIT_LINE[1]), int(CIRCUIT_LINE[2]), max(0, min(255, alpha)))
            
            # Draw connection line with glow effect
            if connection['active']:
                # Main line
                pygame.draw.line(surface, color, start_pos, end_pos, CIRCUIT_LINE_WIDTH)
                
                # Glow effect
                glow_alpha = max(0, min(255, alpha // 3))
                glow_color = (int(CIRCUIT_NODE[0]), int(CIRCUIT_NODE[1]), int(CIRCUIT_NODE[2]), glow_alpha)
                pygame.draw.line(surface, glow_color, start_pos, end_pos, CIRCUIT_LINE_WIDTH + 4)
        
        # Draw nodes
        for node in self.nodes:
            pos = (node['pos'][0] + offset[0], node['pos'][1] + offset[1])
            
            # Calculate pulse effect
            pulse = 0.5 + 0.5 * math.sin(node['pulse_phase'])
            alpha = int(150 + 105 * pulse * self.glow_intensity)
            
            if node['active']:
                # Active node with glow
                node_color = (*CIRCUIT_NODE, alpha)
                glow_color = (*CIRCUIT_NODE, alpha // 4)
                
                # Draw glow
                pygame.draw.circle(surface, glow_color, pos, CIRCUIT_NODE_RADIUS + 6)
                pygame.draw.circle(surface, glow_color, pos, CIRCUIT_NODE_RADIUS + 3)
                
                # Draw main node
                pygame.draw.circle(surface, node_color, pos, CIRCUIT_NODE_RADIUS)
            else:
                # Inactive node
                node_color = (*CIRCUIT_LINE, alpha // 2)
                pygame.draw.circle(surface, node_color, pos, CIRCUIT_NODE_RADIUS // 2)

class GeometricPattern:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.shapes = []
        self.animation_time = 0
        
        self.generate_shapes()
    
    def generate_shapes(self):
        """Generate geometric shapes for background decoration"""
        num_shapes = 20
        
        for _ in range(num_shapes):
            shape_type = random.choice(GEOMETRIC_SHAPES)
            color = random.choice(GEOMETRIC_COLORS)
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(20, 60)
            
            shape = {
                'type': shape_type,
                'pos': (x, y),
                'size': size,
                'color': color,
                'rotation': random.uniform(0, 2 * math.pi),
                'rotation_speed': random.uniform(-1, 1),
                'pulse_phase': random.uniform(0, 2 * math.pi)
            }
            self.shapes.append(shape)
    
    def update(self, dt):
        """Update geometric pattern animation"""
        self.animation_time += dt
        
        for shape in self.shapes:
            shape['rotation'] += shape['rotation_speed'] * dt
            shape['pulse_phase'] += dt * 0.5
            if shape['pulse_phase'] > 2 * math.pi:
                shape['pulse_phase'] -= 2 * math.pi
    
    def draw(self, surface, offset=(0, 0)):
        """Draw geometric shapes"""
        for shape in self.shapes:
            pos = (shape['pos'][0] + offset[0], shape['pos'][1] + offset[1])
            
            # Calculate opacity based on pulse
            pulse = 0.3 + 0.7 * math.sin(shape['pulse_phase'])
            alpha = int(255 * GEOMETRIC_OPACITY * pulse)
            
            # Create color with alpha - ensure it's a proper RGBA tuple with valid values
            base_color = shape['color']
            color = (int(base_color[0]), int(base_color[1]), int(base_color[2]), max(0, min(255, alpha)))
            
            # Create a temporary surface for the shape
            temp_surface = pygame.Surface((shape['size'] * 2, shape['size'] * 2), pygame.SRCALPHA)
            
            if shape['type'] == 'triangle':
                self.draw_triangle(temp_surface, (shape['size'], shape['size']), shape['size'], color, shape['rotation'])
            elif shape['type'] == 'square':
                self.draw_square(temp_surface, (shape['size'], shape['size']), shape['size'], color, shape['rotation'])
            elif shape['type'] == 'hexagon':
                self.draw_hexagon(temp_surface, (shape['size'], shape['size']), shape['size'], color, shape['rotation'])
            elif shape['type'] == 'circle':
                pygame.draw.circle(temp_surface, color, (shape['size'], shape['size']), shape['size'])
            
            # Blit the shape to the main surface
            surface.blit(temp_surface, (pos[0] - shape['size'], pos[1] - shape['size']))
    
    def draw_triangle(self, surface, center, size, color, rotation):
        """Draw a rotated triangle"""
        points = [
            (center[0], center[1] - size),
            (center[0] - size * 0.866, center[1] + size * 0.5),
            (center[0] + size * 0.866, center[1] + size * 0.5)
        ]
        
        # Rotate points
        rotated_points = []
        for point in points:
            dx = point[0] - center[0]
            dy = point[1] - center[1]
            new_x = dx * math.cos(rotation) - dy * math.sin(rotation) + center[0]
            new_y = dx * math.sin(rotation) + dy * math.cos(rotation) + center[1]
            rotated_points.append((new_x, new_y))
        
        pygame.draw.polygon(surface, color, rotated_points)
    
    def draw_square(self, surface, center, size, color, rotation):
        """Draw a rotated square"""
        points = [
            (center[0] - size, center[1] - size),
            (center[0] + size, center[1] - size),
            (center[0] + size, center[1] + size),
            (center[0] - size, center[1] + size)
        ]
        
        # Rotate points
        rotated_points = []
        for point in points:
            dx = point[0] - center[0]
            dy = point[1] - center[1]
            new_x = dx * math.cos(rotation) - dy * math.sin(rotation) + center[0]
            new_y = dx * math.sin(rotation) + dy * math.cos(rotation) + center[1]
            rotated_points.append((new_x, new_y))
        
        pygame.draw.polygon(surface, color, rotated_points)
    
    def draw_hexagon(self, surface, center, size, color, rotation):
        """Draw a rotated hexagon"""
        points = []
        for i in range(6):
            angle = i * math.pi / 3 + rotation
            x = center[0] + size * math.cos(angle)
            y = center[1] + size * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points) 