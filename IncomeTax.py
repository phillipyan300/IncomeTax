from tkinter import *
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

root = Tk()
root.title("Income Taxes Simulation")

def FullBracket(income1, taxrate1, income2, taxrate2):
  bracket_tax = ((income2 - income1)*(taxrate2 + taxrate1))/2
  return bracket_tax

# This function inds the total value of tax paid in the the tax bracket if user is in the tax bracket.
def PartialBracket(income1, taxrate1, income2, taxrate2, user_income):
  slope = (taxrate2-taxrate1)/(income2-income1)
  user_margtaxrate = slope*(user_income-income1) + taxrate1
  user_brackettax = ((user_income - income1)*(user_margtaxrate + taxrate1))/2
  return user_brackettax


# This function calculates average tax rate.
def AvgTaxRate(total_tax, user_income):
    avg_tax_rate = total_tax/user_income
    return avg_tax_rate


# this funcion finds how many times the function FullBracket will run
def runtimes_FullBracket(income_endpoints, user_income):
    x = 1
    counter = 0
    while user_income > income_endpoints[x]:
        counter += 1
        if income_endpoints[-1] == income_endpoints[x]:
            break
        x += 2

    return counter


# main fucntion that runs everything
def main(income_endpoints, taxrate_endpoints, user_income):
    total_tax = 0
    avg_tax_rate = 0

#This below is the number of times that we will run the full bracket
    overbrackets = runtimes_FullBracket(income_endpoints,user_income)
    #Full Brackets
    z = overbrackets
    while z > 0:
        total_tax += FullBracket(income_endpoints[2*z-2], taxrate_endpoints[2*z-2], income_endpoints[2*z- 1], taxrate_endpoints[2*z -1])
        z -= 1

    #Partial Brackets
    y = overbrackets
    if user_income > income_endpoints[-1]:
      mid = user_income - income_endpoints[-1]
      over = mid * taxrate_endpoints[-1]
      total_tax += over
    else:
        total_tax += PartialBracket(income_endpoints[2*y], taxrate_endpoints[2*y], income_endpoints[2*y + 1], taxrate_endpoints[2*y + 1], user_income)

    return total_tax
#Finally the average tax rate

# [0-9700],[9701-39475], etc are the brackets.
us_income_endpoints = [0, 9700, 9701, 39475, 39476, 84200, 84201, 160725, 160726, 204100, 204101, 510300]
us_taxrate_endpoints = [0.1, 0.1, 0.12, 0.12, 0.22, 0.22, 0.24, 0.24, 0.32, 0.32, 0.35, 0.35, 0.37]
#note: the taxrate endpoints have one more value than the income endpoints, in this case 37%, because anything aobve the highest tax bracket is taxed at 37$

#note: these are all in euros
german_income_endpoints = [0, 9407, 9408, 57050, 57051, 270500]
german_taxrate_endpoints = [0, 0, 0.14, 0.42, 0.42, 0.45, 0.45]

#note: These are in rmb
china_income_endpoints = [0, 2999, 3000, 11999, 12000, 24999, 25000, 34999, 35000, 54999, 55000, 79999]
china_taxrate_endpoints = [0.03, 0.03, 0.1, 0.1, 0.2, 0.2, 0.25, 0.25, 0.3, 0.3, 0.35, 0.35, 0.45]

#Peruvian soles
peru_income_endpoints = [0, 21000, 21000, 84000, 84000, 147000, 147000, 189000]
peru_taxrate_endpoints = [0.08, 0.08, 0.14, 0.14, 0.17, 0.17, 0.2, 0.2, 0.3]

def marg_ave_graph(income_endpoints, taxrate_endpoints):
    #Some Structural Graph stuff
    #Find which country it is
    if income_endpoints == german_income_endpoints:
        w = "in Germany"
    elif income_endpoints == us_income_endpoints:
        w = "in the United States"
    elif income_endpoints == china_income_endpoints:
        w = "in China"
    elif income_endpoints == peru_income_endpoints:
        w = "in Peru"
    # giving a title to my graph
    plt.title("Marginal and Average Income Tax Rates as a function of Taxable Income " + w)
    # naming the x axis
    #MAYBE ADD TAXABLE INCOME IN (YUAN, peso ect)
    plt.xlabel("Taxable Income")
    # naming the y axis
    plt.ylabel("Tax Rate in Percent")

    #Marginal Tax Line
    linex1 = income_endpoints
    liney1 = taxrate_endpoints
    #Just adding some points to x and y so that it matches up with y and shows the tax bracket that goes to infinity
    linex1.append(income_endpoints[-1]+1)
    linex1.append(round(income_endpoints[-1]*1.1))
    liney1.append(taxrate_endpoints[-1])
    plt.plot(linex1, liney1, label = "Marginal Tax Rate")

    #Average Tax Line
    linex2 = []
    liney2 = []
    #X is the user income at a given point. Below for function calculates the user income and avg tax for all points
    for x in range(1, round(income_endpoints[-1]*1.1)):
        avgtaxrate = main(income_endpoints, taxrate_endpoints, x)/x
        linex2.append(x)
        liney2.append(avgtaxrate)
    plt.plot(linex2, liney2, label = "Average Tax Rate")
    # legend
    plt.legend()
    plt.show()

def derivative_after_pre_tax(income_endpoints, taxrate_endpoints):
    xvalue=[]
    slope_list = []
    for x in range(2, round(income_endpoints[-1] * 1.1), 100):
        #Use the limit definition of a derivative, approximation with lim as a = 2
        #delta Aftertax is the change in y value, 2 is the delta x
        #Caculating the derivative approximation
        totaltax1 = main(income_endpoints, taxrate_endpoints, x-1)
        aftertax1 = (x-1) - totaltax1
        totaltax2 = main(income_endpoints, taxrate_endpoints, x+1)
        aftertax2 = x+1 -totaltax2
        slope_at_x = (aftertax2-aftertax1)/2
        #adding to the x and slope list
        xvalue.append(x)
        slope_list.append(slope_at_x)
        #slope starts at 2, so need to pop first in x value list to stay the same
   #start graph
    if income_endpoints == german_income_endpoints:
        b = "in Germany"
    elif income_endpoints == us_income_endpoints:
        b = "in the United States"
    elif income_endpoints == china_income_endpoints:
        b = "in China"
    elif income_endpoints == peru_income_endpoints:
        b = "in Peru"
    # giving a title to my graph
    plt.title("After Tax Income as a function of Taxable Income " + b)
    # MAYBE ADD TAXABLE INCOME IN (YUAN, peso ect)
    plt.xlabel("Taxable Income")
    # naming the y axis
    plt.ylabel("After Tax Income")
    plt.plot(xvalue, slope_list)
    plt.show()
###########
#
#
#
#Tkinter stuff

#Introduction
intro = """Welcome to our Income Taxes Simulation. By Phillip Yan, Matthew Cheng, and John Zammit \n
This program will help you understand how income taxes work on both a micro and a macro level. 
As an individual, the program will help you calculate the amount of tax you need to pay based on your income, and also 
calculate the average rate of the tax. 
At the same time, in this simulation, you'll be able to understand how differences between income tax structures impact 
both the individual's pocketbook and productivity within the economy as a whole, with concepts like the Laffer Curve"""

introinfo = Label(root, text = intro)
introinfo.grid(row=0, column=1)

#This is basically setting up windwos to open after clicking buttons
#First winodw is for calculating taxes
def open_window1():
    top = Toplevel()
    top.title("Income Tax Calculator")
    #The intro
    intro= """This program will help you calculate the amount of tax you need to pay based on your local tax bracket, and also calculate the average rate of the tax.
Income tax brackets are usually expressed in terms of marginal tax rates, or the tax rate at which a certain bracket of income is taxed. This can be quite hassle for the average american who is looking to file taxes. 
While it isn't a complete guide to the deductions, caveats and exceptions of byzantine income tax systems, the average tax is usually a better function to use when calculating the amount of tax to pay in taxes. 
 Please remember to use local currency and only enter numbers
 Please start by choosing a country"""

    intro1 = Label(top, text=intro)
    intro1.grid(row=0, column=0)

    #Space for formatting
    whitespace = Label(top, text="   ")
    whitespace.grid(row=1, column=0)

    # Ask for country
    clicked = StringVar()
    clicked.set("Choose a country")

    drop = OptionMenu(top, clicked, "United States", "Germany", "China", "Peru")
    drop.grid(row=2, column=0)

    askincome = Entry(top, borderwidth=5)
    askincome.grid(row=3, column =0)

    #Calculate tax
    def calculate_tax():
        #Figuring out which country
        if clicked.get() == "United States":
            income_endpoints_used = us_income_endpoints
            taxrate_endpoints_used = us_taxrate_endpoints
        elif clicked.get() == "Germany":
            income_endpoints_used = german_income_endpoints
            taxrate_endpoints_used = german_taxrate_endpoints
        elif clicked.get() == "China":
            income_endpoints_used = china_income_endpoints
            taxrate_endpoints_used = china_taxrate_endpoints
        else:
            income_endpoints_used = peru_income_endpoints
            taxrate_endpoints_used = peru_taxrate_endpoints
        #Figuring out tax rate
        total_tax = main(income_endpoints_used, taxrate_endpoints_used, int(askincome.get()))
        average_tax_rate = total_tax/int(askincome.get())
        text = "Your total tax amount to be paid is " + str(round(total_tax)) + " and your average tax rate is " + str(round((average_tax_rate)*100)) + "%"
        text1 = Label(top, text = text)
        text1.grid(row=5, column=0)



    reveal_tax = Button(top, text = "Calculate the amount of tax you have to pay", command = calculate_tax)
    reveal_tax.grid(row=4, column=0)



#Second window is for comparing countries
def open_window2():
    top = Toplevel()
    top.title("Comparing income tax brackets from around the world")
    #The intro
    intro = "Here you can compare two different income tax brackets from around the world side to side. \n Just choose two countries from the dropdown menu"
    intro1 = Label(top, text = intro)
    intro1.grid(row=0, column=1)
    #choosing two countries to compare

    clicked1 = StringVar()
    clicked1.set("Choose a country")
    clicked2 = StringVar()
    clicked2.set("Choose a country")

    drop1 = OptionMenu(top, clicked1, "United States", "Germany", "China", "Peru")
    drop1.grid(row=1, column=0)
    drop2 = OptionMenu(top, clicked2, "United States", "Germany", "China", "Peru")
    drop2.grid(row=1, column=2)

    #Displaying the graphs
    def compare_graphs():
        #First for the first dropdown menu
        if clicked1.get() == "United States":
            income_endpoints_used1 = us_income_endpoints
            taxrate_endpoints_used1 = us_taxrate_endpoints
        elif clicked1.get() == "Germany":
            income_endpoints_used1 = german_income_endpoints
            taxrate_endpoints_used1 = german_taxrate_endpoints
        elif clicked1.get() == "China":
            income_endpoints_used1 = china_income_endpoints
            taxrate_endpoints_used1 = china_taxrate_endpoints
        else:
            income_endpoints_used1 = peru_income_endpoints
            taxrate_endpoints_used1 = peru_taxrate_endpoints

        #Second for the second dropdown menu
        if clicked2.get() == "United States":
            income_endpoints_used2 = us_income_endpoints
            taxrate_endpoints_used2 = us_taxrate_endpoints
        elif clicked2.get() == "Germany":
            income_endpoints_used2 = german_income_endpoints
            taxrate_endpoints_used2 = german_taxrate_endpoints
        elif clicked2.get() == "China":
            income_endpoints_used2 = china_income_endpoints
            taxrate_endpoints_used2 = china_taxrate_endpoints
        else:
            income_endpoints_used2 = peru_income_endpoints
            taxrate_endpoints_used2 = peru_taxrate_endpoints
        #Plot?
        marg_ave_graph(income_endpoints_used1, taxrate_endpoints_used1)
        marg_ave_graph(income_endpoints_used2, taxrate_endpoints_used2)




    reveal_graphs = Button(top, text="Compare", command=compare_graphs)
    reveal_graphs.grid(row = 2, column =1)


#Third window is for scenarios
def open_window3():
    top = Toplevel()
    top.title("Fiscal Policy and Taxes")
    # The intro
    intro = """In times of rapid growth or economic decline, governments often change the income tax policy to adjust the economy back into equilibrium.
Below are some examples of the possible paths that government may take.
Using the income tax bracket of the United States, we will see how such policies will impact your bottom line"""
    intro1 = Label(top, text = intro)
    intro1.grid(row=0, column=0)
    #Scenerios

    #Scenario 1
    text = """In light of the COVID-19 Pandemic, the US decides to decrease the marginal tax rate for the 
second and third tax brackets by 10%. Enter your income to see how this will impact you """
    introscenario1 = Label(top, text = text)
    introscenario1.grid(row=1, column=0)
    askincome1 = Entry(top, borderwidth=5)
    askincome1.grid(row=2, column=0)
    #New US income tax bracket

    #Button to answer
    def calculate_tax():
        #Old tax bracket
        new_us_taxrate_endpoints = [0.1, 0.1, 0.02, 0.02, 0.12, 0.12, 0.24, 0.24, 0.32, 0.32, 0.35, 0.35, 0.37]
        old_total_tax = main(us_income_endpoints, us_taxrate_endpoints, int(float(askincome1.get())))
        old_average_tax_rate = old_total_tax / int(askincome1.get())
        #New Tax Bracket
        total_tax = main(us_income_endpoints, new_us_taxrate_endpoints, int(float(askincome1.get())))
        average_tax_rate = total_tax / int(float(askincome1.get()))
        #because the line was too long so 2 variables
        text = "Your new tax amount to be paid is " + str(round(total_tax)) + " and your new average tax rate is " + str(round(average_tax_rate*100)) + "%."
        textpart2 = " You saved $" + str(round(old_total_tax-total_tax)) +" and you average tax rate decreased by " + str(round((old_average_tax_rate-average_tax_rate)*100) ) + "%!"
        actualtext = text + textpart2
        text1 = Label(top, text=actualtext)
        text1.grid(row=4, column=0)
        if old_total_tax-total_tax == 0:
            text2 = Label(top, text = "Unfortunately, you weren't eligible for the tax reduction")
            text2.grid(row = 5, column=0)
    scenerio1 = Button(top, text="Click here calculate the impacts", command = calculate_tax)
    scenerio1.grid(row=3, column=0)


    #Scenario 2
    text2 = """The government believes that the third tax bracket is ineffective, 
and should be combined with the fourth lowest tax bracket, with the income being taxed at rate of the fourth bracket. Enter your income to see whether or not this will impact you"""
    introscenario2 = Label(top, text=text2)
    introscenario2.grid(row=6, column=0)
    askincome = Entry(top, borderwidth=5)
    askincome.grid(row=7, column=0)
    # New US income tax bracket
    def calculate_tax1():
        #Old tax bracket
        new_us_taxrate_endpoints = [0.1, 0.1, 0.12, 0.12, 0.24, 0.24, 0.24, 0.24, 0.32, 0.32, 0.35, 0.35, 0.37]
        old_total_tax = main(us_income_endpoints, us_taxrate_endpoints, int(float(askincome.get())))
        old_average_tax_rate = old_total_tax / int(askincome.get())
        #New Tax Bracket
        total_tax = main(us_income_endpoints, new_us_taxrate_endpoints, int(float(askincome.get())))
        average_tax_rate = total_tax / int(float(askincome.get()))
        #because the line was too long so 2 variables
        text = "Your new tax amount to be paid is " + str(round(total_tax)) + " and your new average tax rate is " + str(round(average_tax_rate*100)) + "%."
        textpart2 = " You paid $" + str((round(old_total_tax-total_tax))*-1) +" more and you average tax rate increased by " + str(round((old_average_tax_rate-average_tax_rate)*-100) ) + "%"
        actualtext = text + textpart2
        text1 = Label(top, text=actualtext)
        text1.grid(row=9, column=0)
        if old_total_tax-total_tax == 0:
            text2 = Label(top, text = "Fortunately, you weren't eligible for the tax hike")
            text2.grid(row = 10, column=0)
    scenerio2 = Button(top, text="Click here calculate the impacts", command = calculate_tax1)
    scenerio2.grid(row = 8, column=0)

    #Scenerio 3
    text3 = """The government has given you a 25% tax credit, meaning you will be only taxed up to 75% of your income.
How will this affect your taxes?"""
    introscenario3 = Label(top, text=text3)
    introscenario3.grid(row=11, column=0)
    askincome3 = Entry(top, borderwidth=5)
    askincome3.grid(row=12, column=0)
    def calculate_tax2():
        #Pre tax credit
        old_total_tax = main(us_income_endpoints, us_taxrate_endpoints, int(float(askincome3.get())))
        old_average_tax_rate = old_total_tax / int(askincome3.get())
        #POst tax credit
        total_tax = main(us_income_endpoints, us_taxrate_endpoints, int(float(askincome2.get())*0.75))
        average_tax_rate = total_tax / int(askincome2.get())
        #Extra long text line
        text = "Your new tax amount to be paid is " + str(round(total_tax)) + " and your new average tax rate is " + str(round(average_tax_rate * 100)) + "%."
        textpart2 = " You paid $" + str((round(old_total_tax - total_tax)) * 1) + " less and you average tax rate decresaed by " + str(round((old_average_tax_rate - average_tax_rate) * 100)) + "%"
        textpart3 = ". Everyone is eligible for this deduction!"
        actualtext = text + textpart2 + textpart3
        text1 = Label(top, text=actualtext)
        text1.grid(row=14, column=0)
    scenerio3 = Button(top, text="Click here calculate the impacts", command=calculate_tax2)
    scenerio3.grid(row=13, column=0)

def open_window4():
    top = Toplevel()
    top.title("Income Taxes and Worker Productivity")
    # The intro
    intro = """When governments increase taxes, they must not forget the impacts of the taxes on worker productivity. 
Every percent increase revenue is a corresponding percent decrease in the disposable income of workers. 
Should the government tax to heavily, the workers may be disincentivized to work. We built a model to explain this phenomenon 
through the concept of diminishing returns per marginal dollar earned. The four countries can thus be compared in this regard """
    intro1 = Label(top, text=intro)
    intro1.grid(row=0, column=0)
    #Now for the dropdown menu
    clicked = StringVar()
    clicked.set("Choose a country")

    drop1 = OptionMenu(top, clicked, "United States", "Germany", "China", "Peru")
    drop1.grid(row=1, column=0)
    #function to show the derivative graph
    def show_graphs():
        if clicked.get() == "United States":
            income_endpoints_used1 = us_income_endpoints
            taxrate_endpoints_used1 = us_taxrate_endpoints
        elif clicked.get() == "Germany":
            income_endpoints_used1 = german_income_endpoints
            taxrate_endpoints_used1 = german_taxrate_endpoints
        elif clicked.get() == "China":
            income_endpoints_used1 = china_income_endpoints
            taxrate_endpoints_used1 = china_taxrate_endpoints
        else:
            income_endpoints_used1 = peru_income_endpoints
            taxrate_endpoints_used1 = peru_taxrate_endpoints
        #Plot
        derivative_after_pre_tax(income_endpoints_used1, taxrate_endpoints_used1)

    show_graphs = Button(top, text="Click to open", command=show_graphs)
    show_graphs.grid(row=2, column=1)



whitespace = Label(root, text = "       ")
whitespace.grid(row=1, column=0)

#Main home buttons
option1 = Button(root, text="Find how much tax you have to pay", pady = 20, padx = 50, command=open_window1)
option1.grid(row=2, column=0)

option2 = Button(root, text="Compare income tax brackets from around the world", pady = 20, padx = 50, command=open_window2)
option2.grid(row=2, column=1)

option3 = Button(root, text="Find out how fiscal policy affects income taxes", pady = 20, padx = 50, command=open_window3)
option3.grid(row=2, column=2)

option4 = Button(root, text="Compare the effects of different income tax systems on worker productivity", pady = 20, padx = 50, command=open_window4)
option4.grid(row=3, column=1)

my_img = ImageTk.PhotoImage(Image.open("Taxbetter.jpg"))
image_label = Label(image=my_img)
image_label.grid(row = 4, column =1)

#Quit Button
button_quit = Button(root, text = "Exit Program", command = root.quit)
button_quit.grid(row = 0, column = 0)




root.mainloop()