import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QDockWidget, QHBoxLayout
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage
from matplotlib.offsetbox import AnnotationBbox


class AboutNetworkWidget(QWidget):
    def __init__(self, parent=None):
        super(AboutNetworkWidget, self).__init__(parent)
        self.info_label = InfoLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        self.setLayout(layout)

class InfoLabel(QLabel):
    def __init__(self, parent=None):
        super(InfoLabel, self).__init__(parent)
        self.setWordWrap(True)

    def update_info_label(self, text):
        self.setText(text)

class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super(GraphWidget, self).__init__(parent)
        self.figure = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.selected_node = None
        self.pos = None
        self.info_label = None

    def get_node_image(self, node_name, connection_type=None):
        if node_name == 'server':
            return 'server.png'
        elif node_name == 'route':
            return 'route.png'
        elif node_name == 'pc':
            if connection_type == 'LAN':
                return 'pc_lan.png'
            elif connection_type == 'Wireless':
                return 'pc_wireless.png'
        return None

    def get_status_image(self, status):
        if status == 1:
            return 'green.png'
        elif status == 0:
            return 'red.png'
        return None

    def plot_graph(self):
        conn = sqlite3.connect('server_control.db')
        cursor = conn.cursor()

        cursor.execute('SELECT server_name FROM server')
        server_name = cursor.fetchone()[0]

        G = nx.DiGraph()
        G.add_node(server_name, subset=0, image=self.get_node_image('server'))

        cursor.execute('SELECT ip_route, route_name, status FROM route')
        routes = cursor.fetchall()

        for route in routes:
            route_ip = route[0]
            route_name = route[1]
            route_status = route[2]
            G.add_node(route_name, subset=1, image=self.get_node_image('route'))

            if route_status == 0:
                color = 'red'
            else:
                color = 'green'

            G.add_edge(server_name, route_name, color=color)

            cursor.execute('SELECT pc_name, connection_type FROM pc WHERE ip_route = ?', (route_ip,))
            pcs = cursor.fetchall()

            for pc in pcs:
                pc_name = pc[0]
                connection_type = pc[1]
                G.add_node(pc_name, subset=2, image=self.get_node_image('pc', connection_type))
                G.add_edge(route_name, pc_name, color=color, connection_type=connection_type)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        self.pos = nx.multipartite_layout(G, subset_key="subset", align='horizontal', scale=8.0)

        for u, v, attrs in G.edges(data=True):
            connection_type = attrs.get('connection_type')
            if connection_type == 'LAN':
                linestyle = '-'
            elif connection_type == 'Wireless':
                linestyle = 'dashed'
            else:
                linestyle = '-'

            nx.draw_networkx_edges(G, self.pos, edgelist=[(u, v)], width=1, alpha=1, edge_color=attrs['color'], ax=ax,
                                   style=linestyle, arrowstyle='-')

        for node in G.nodes:
            node_pos = self.pos[node]
            node_image = G.nodes[node]['image']
            if node_image:
                img = Image.open(node_image)
                img = img.resize((180, 180))
                imagebox = OffsetImage(img, zoom=0.1)
                ab = AnnotationBbox(imagebox, node_pos, xycoords='data', frameon=False)
                ax.add_artist(ab)
            ax.annotate(node, xy=node_pos, xytext=(node_pos[0], node_pos[1] - 0.2), textcoords='data', ha='center',
                        va='top', fontsize=8)

        ax.set_title('Server Control Graph')
        ax.axis('off')

        self.canvas.draw()

    def node_clicked(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        for node, (nx, ny) in self.pos.items():
            if x - 0.1 <= nx <= x + 0.1 and y - 0.1 <= ny <= y + 0.1:
                self.selected_node = node
                self.update_info_label()
                break

    def update_info_label(self):
        
        if self.selected_node:
            conn = sqlite3.connect('server_control.db')
            cursor = conn.cursor()
            cursor.execute('SELECT server_name FROM server')
            server = [item[0] for item in cursor.fetchall()]
            cursor.execute('SELECT route_name FROM route')
            routes = [item[0] for item in cursor.fetchall()]

            if self.selected_node in server:
                cursor.execute('SELECT * FROM server WHERE server_name = ?', (self.selected_node,))
                result = cursor.fetchone()
                if result:
                    text = f"<b>Имя сервера:</b> {result[2]}<br><b>IP-адрес:</b> {result[1]}<br><b>Internet-IP:</b> {result[4]}"
            elif self.selected_node in routes:
                cursor.execute('SELECT * FROM route WHERE route_name = ?', (self.selected_node,))
                result = cursor.fetchone()
                if result:
                    status = "Online" if result[4] == 1 else "Offline"
                    status_image = self.get_status_image(result[4])
                    if status_image:
                        status_image_html = f"<img src='{status_image}' width='8' height='8'>"
                    else:
                        status_image_html = ""
                    text = f"<b>Имя в локальной сети:</b> {result[2]}<br><b>Статус:</b> {status_image_html} {status} <br><b>IP-адрес:</b> {result[1]}"
            else:
                cursor.execute('SELECT * FROM pc WHERE pc_name = ?', (self.selected_node,))
                result = cursor.fetchone()
                route_element = result[-2]
                if result:
                    cursor.execute('SELECT route_name FROM route WHERE id_route = ?', (route_element,))
                    route_name = cursor.fetchone()
                    if route_name:
                        route_name = route_name[0]
                        status = "Online" if result[7] == 1 else "Offline"
                        status_image = self.get_status_image(result[7])
                        if status_image:
                            status_image_html = f"<img src='{status_image}' width='8' height='8'>"
                        else:
                            status_image_html = ""
                        text = f"<b>IP-адрес:</b> {result[1]}<br><b>Имя в локальной сети:</b> {result[2]}<br><b>Статус:</b> {status_image_html} {status} <br><b>Тип подключения:</b> {result[-4]}<br><b>Имя роутера:</b> {route_name}"
            self.info_label.setText(text)
            
            
            


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.graph_widget = GraphWidget()
        self.setCentralWidget(self.graph_widget)

        self.about_network_widget = AboutNetworkWidget()
        self.graph_widget.info_label = self.about_network_widget.info_label
        
        layout = QHBoxLayout()
        layout.addWidget(self.graph_widget)
        layout.addWidget(self.about_network_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.graph_widget.plot_graph()
        self.graph_widget.canvas.mpl_connect('button_press_event', self.graph_widget.node_clicked)
        print(self.graph_widget.node_clicked, layout, self.graph_widget, self.about_network_widget, sep="+++")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
