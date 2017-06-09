Rook, King, Pawn, Queen, Horse = ['r', 'k', 'p', 'q', 'h']

if material == Material.Queen:
    moves = self.queen_move(turn, location)
    if moves != []:
        total_moves.extend(moves)
if material == Material.Horse:
    moves = self.horse_move(turn, location)
    if move != []:
        total_moves.extend(moves)

def horse_move(self, turn, location_1):
        moves = []
        x = location_1[0]
        y = location_1[1]
        if y > 1:
            y1 = y - 2
            if x != 0:
                x1 = x - 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
            if x != 8:
                x1 = x + 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
        if y < 6:
            y1 = y + 2
            if x != 0:
                x1 = x - 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
            if x != 8:
                x1 = x + 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
        if x > 1:
            x1 = x - 2
            if y != 0:
                y1 = y - 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
            if y != 8:
                y1 = y + 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
        if x < 6:
            x1 = x + 2
            if y != 0:
                y1 = y - 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
            if y != 8:
                y1 = y + 1
                location_2 = (x1, y1)
                if self.check_occupied_by_self(location_2) == 0:
                    move = (location_1, location_2)
                    moves.append(move)
        return moves

def queen_move(self, turn, location_1):
        moves = []
        location_2 = list(location_1)
        rook_moves = self.rook_move(turn,location_1)
        moves.extend(rook_moves)
        while location_2[0] != 7 and location_2[1] != 0:
            location_2[0] += 1
            location_2[1] -= 1
            if self.check_occupied_by_self(tuple(location_2)) == 0:
                moves.append([location_1, tuple(location_2)])
            else:
                break
            if self.check_occupied_by_other(tuple(location_2)) == 1:
                break
        location_2 = list(location_1)
        while location_2[0] != 7 and location_2[1] != 7:
            location_2[0] += 1
            location_2[1] += 1
            if self.check_occupied_by_self(tuple(location_2)) == 0:
                moves.append([location_1, tuple(location_2)])
            else:
                break
            if self.check_occupied_by_other(tuple(location_2)) == 1:
                break
        location_2 = list(location_1)
        while location_2[0] != 0 and location_2[1] != 7:
            location_2[0] -= 1
            location_2[1] += 1
            if self.check_occupied_by_self(tuple(location_2)) == 0:
                moves.append([location_1, tuple(location_2)])
            else:
                break
            if self.check_occupied_by_other(tuple(location_2)) == 1:
                break
        location_2 = list(location_1)
        while location_2[0] != 0 and location_2[1] != 0:
            location_2[0] -= 1
            location_2[1] -= 1
            if self.check_occupied_by_self(tuple(location_2)) == 0:
                moves.append([location_1, tuple(location_2)])
            else:
                break
            if self.check_occupied_by_other(tuple(location_2)) == 1:
                break
        return moves


if material == Material.Queen:
    if side == Side.White:
        score += 50
    else:
        score -= 50