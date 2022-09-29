#--------------------------------------------------------------------------------
# Load module
#--------------------------------------------------------------------------------
from ...params   import Settings

#--------------------------------------------------------------------------------
# class CheckImageCollection
#--------------------------------------------------------------------------------
class CheckImageCollection:

    #--------------------------------------------------------------------------------
    # class List
    #--------------------------------------------------------------------------------
    class List:

        # input
        def input(input):

            # Display status
            print(" - Searching : ", end="")

            # Check keywords
            if type(input) != list:
                raise Exception("Error! keywords types must be list")
            if not input:
                raise Exception("Error! At least keywords need one word")

            # Finish
            return 1

        # output
        def output(output):

            # Check URL list
            if not output:
                raise Exception("Error! No image collection found!")

            # Display status
            print(f"{len(output)} image collections found!")

            # Finish
            return 1


    #--------------------------------------------------------------------------------
    # class Date
    #--------------------------------------------------------------------------------
    class Date:

        # input
        def input(input):

            # Display status
            print(" - Date : ", end="")

            # Finish
            return 1

        # output
        def output(output):

            # Check DATE list
            if not output:
                raise Exception("Error! No date list found!")

            if len(output) > Settings.date_num_max:
                message = f"datenum: {len(output)} , datenum_max: {Settings.date_num_max}"
                raise Exception("Error! Date number is too large!\n"+message)

            # Display status
            for i in range(len(output)):
                print(f"{output[i]}, ", end="")
            print("")

            # Finish
            return 1            

    #--------------------------------------------------------------------------------
    # class Ppu
    #--------------------------------------------------------------------------------
    class Ppu:

        # input
        def input(val_data,input):

            # Display status
            print(" - Resolution : ", end="")

            # Check input variable1
            if not val_data:
                raise Exception("Error! Please use method filterDate before filterResolution")        

            # Check input variable2

            # Finish
            return 1

        # output
        def output(output1,output2):

            # Display status
            print(f"{output2} pixels per {output1.unit} {output1.unit_str} ")        

            # Finish
            return 1

    #--------------------------------------------------------------------------------
    # class Bounds
    #--------------------------------------------------------------------------------
    class Bounds:

        # input
        def input(val_data,input1,input2):

            # Display status
            print(" - Bounds : ", end="")

            # Check Input variable
            if not val_data:
                raise Exception("Error! Please use method filterResolution before filterBounds") 

            # Check input variable1

            # Finish
            return 1

        # output
        def output(output,bbox):

            # Check bounds URL list
            if (output == [[]]) or (output == []):
                message = f"bbox : {bbox}"
                raise Exception("Error! No COGs in bounds found!\n"+message)

            # Display status
            print(bbox)
            #for i in range(len(stac_bounds_url)):
            #    print(f"{len(stac_bounds_url[i])} COGs, ", end="")
            #print("")

            # Finish
            return 1

    #--------------------------------------------------------------------------------
    # class Band
    #--------------------------------------------------------------------------------
    class Band:

        # input
        def input(val_data,input1):

            # Display status
            print(" - Band : ", end="")

            # Check Input variable
            if not val_data:
                raise Exception("Error! Please use method filterBounds before select")

            # Finish
            return 1

        # output
        def output(output):

            # Display status
            print(output)

            # Finish
            return 1            
