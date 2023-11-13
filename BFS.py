from collections import deque
from Utility import Node
from Algorithm import Algorithm


class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        # Khởi tạo trạng thái ban đầu và trạng thái mục tiêu
        initialstate, goalstate = self.get_initstate_and_goalstate(snake)

        # Khởi tạo hàng đợi FIFO (First In First Out)
        self.frontier = deque([])
        # Danh sách các trạng thái đã duyệt
        self.explored_set = []
        # Danh sách lưu trữ đường đi từ trạng thái ban đầu đến trạng thái hiện tại
        self.path = []

        # Thêm trạng thái ban đầu vào hàng đợi
        self.frontier.append(initialstate)

        # Lặp cho đến khi không còn trạng thái nào trong hàng đợi
        while len(self.frontier) > 0:
            # Lấy trạng thái ở đầu hàng đợi (trạng thái có mức sâu thấp nhất)
            shallowest_node = self.frontier.popleft()

            # Đánh dấu trạng thái này là đã duyệt
            self.explored_set.append(shallowest_node)

            # Lấy danh sách các trạng thái láng giềng
            neighbors = self.get_neighbors(shallowest_node)

            # Duyệt qua từng trạng thái láng giềng
            for neighbor in neighbors:
                # Kiểm tra xem đường đi đi qua cơ thể con rắn, ra khỏi biên, hoặc đã được duyệt chưa
                if self.inside_body(snake, neighbor) or self.outside_boundary(neighbor) or neighbor in self.explored_set:
                    continue  # Bỏ qua đường đi này

                # Nếu trạng thái láng giềng chưa được thăm
                if neighbor not in self.frontier and neighbor not in self.explored_set:
                    # Đánh dấu trạng thái cha
                    neighbor.parent = shallowest_node
                    # Đánh dấu trạng thái đã duyệt
                    self.explored_set.append(neighbor)
                    # Thêm trạng thái láng giềng vào hàng đợi để kiểm tra các trạng thái con của nó trong vòng lặp tiếp theo
                    self.frontier.append(neighbor)

                    # Kiểm tra xem trạng thái láng giềng có phải là trạng thái mục tiêu không
                    if neighbor.equal(goalstate):
                        # Trả về đường đi từ trạng thái ban đầu đến trạng thái mục tiêu
                        return self.get_path(neighbor)

        # Trường hợp không tìm thấy đường đi
        return None

