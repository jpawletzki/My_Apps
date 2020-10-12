Basic display of OOP programming concepts in C++


#include <iostream>
#include <iomanip>
#include <string>
#include <ctime> 
#include <cstdlib> 
using namespace std;

enum Damage 
{
	WATER_UNBOMBED, WATER_BOMBED,
	SHIP_UNBOMBED, SHIP_BOMBED
};

const char display[] = { '~', 'O', '~', 'X' }; 
const  int WIDTH = 10;
const  int HEIGHT = 10;
Damage grid[HEIGHT][WIDTH];

class CentralCommand
{
private:
	char ans;
	int numHits;
public:
	void instructions();
	bool isGameOver();
	bool playAgain();
};

void CentralCommand::instructions()
{
	cout << "You are about to play battleship." << endl << "There is a 10x10 grid that contains one 3x1 boat that you must sink, faced either horizontally or vertically." << endl <<
		"To bomb a spot, enter 'b', to quit, enter 'q'." << endl;
	return;
}

bool CentralCommand::isGameOver()
{
	numHits = 0;
	for (int y = 0; y < 10; y++)
	{
		for (int z = 0; z < 10; z++)
		{
			if (grid[z][y] == SHIP_BOMBED)
			{
				numHits++;
			}
		}
	}
	if (numHits == 3)
	{
		return true;
	}
	else
	{
		return false;
	}
	

}

bool CentralCommand::playAgain()
{

	cout << endl << "Congratulations, you win" << endl;
	cout << endl << "Do you want to play again? (y/n) ";
	cin >> ans;
	if (ans == 'y') 
	{
		cout << endl;
		return true;
	}
	else
	{
		return false;
	}
}

class GameGrid
{
public:
void initGrid();
void displayGameGrid();
};

void GameGrid::initGrid()
{
	for (int y = 0; y < 10; y++)
	{
		for (int z = 0; z < 10; z++)
		{
			grid[z][y] = WATER_UNBOMBED;
		}
	}
	int direction;
	direction = rand() % 2;
	if (direction == 0)
	{
		int initialSpotLeftRight = rand() % 8;
		int initialYcord = rand() % 10;
		for (int i = initialSpotLeftRight; i < initialSpotLeftRight + 3; i++)
		{
			grid[i][initialYcord] = SHIP_UNBOMBED;
		}
	}
	else
	{
		int initialSpotUpDown = rand() % 8;
		int initialXcord = rand() % 10;
		for (int i = initialSpotUpDown; i < initialSpotUpDown + 3; i++)
		{
			grid[initialXcord][i] = SHIP_UNBOMBED;
		}
	}
	return;
}

void GameGrid::displayGameGrid()
{
	cout << endl;
	cout << "  ";
	for (int x = 0; x < 10; x++)
	{
		cout << x << " ";
	}

	cout << endl;

	for (int y = 0; y < 10; y++)
	{
		cout << y << " ";
		for (int z = 0; z < 10; z++)
		{
			cout << display[grid[z][y]] << " ";
		}
		cout << endl;
	}
	return;
}

class CommandInput
{
private:
	char cmd;
	int xcoord;
	int ycoord;
public:
	void executeCommand();
	void dropBomb(int xcoord,int ycoord);
};

void CommandInput::executeCommand()
{
	int xcoord;
	int ycoord;
	cout << endl << "Please enter your orders sir: ";
	cin >> cmd;
	if (cmd == 'b')
	{
		cout << endl << "Enter x cordinate" << endl;
		cin >> xcoord;
		while (xcoord > 9 || xcoord < 0)
		{
			cout << "Enter a valid coordinate" << endl;
			cin >> xcoord;
		}
		cout << endl << "Enter y cordinate" << endl;
		cin >> ycoord;
		while (ycoord > 9 || ycoord < 0)
		{
			cout << "Enter a valid coordinate" << endl;
			cin >> ycoord;
		}
		cout << endl << "Droping bomb at (X,Y):(" << xcoord << "," << ycoord << ")" << endl;
		dropBomb(xcoord, ycoord);
	}

	if (cmd == 'q')
	{
		exit(0);
	}
	return;
}

void CommandInput::dropBomb(int xcoord,int ycoord) 
{

	if (grid[xcoord][ycoord] == WATER_BOMBED)
	{
		cout << endl << "The spot was already bombed..." << endl;
	}
	if (grid[xcoord][ycoord] == WATER_UNBOMBED)
	{
		grid[xcoord][ycoord] = WATER_BOMBED;
	}

	if (grid[xcoord][ycoord] == SHIP_UNBOMBED)
	{
		grid[xcoord][ycoord] = SHIP_BOMBED;
		cout << endl << "You hit the ship!" << endl;
	}
	return;
}

int main()
{
	CentralCommand GameMaster;
	GameGrid GridMaster;
	CommandInput Input;
	srand(time(0));
	do 
	{
		GameMaster.instructions();
		GridMaster.initGrid();
		GridMaster.displayGameGrid();
		while (GameMaster.isGameOver() == false)
		{
			Input.executeCommand();
			GameMaster.isGameOver();
			GridMaster.displayGameGrid();
		}
	} while (GameMaster.playAgain());
	system("pause");
	return 0;
}



