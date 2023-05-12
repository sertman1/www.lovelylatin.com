def process_unimorph_file():
    inflected_form_to_base_form = {}

    f = open('./latin_processing/lat.txt', 'r')
    for line in f.readlines():
        base_form = ""
        inflected_form = ""

        i = 0
        while line[i] != '\t' and line[i] != " ":
            base_form += line[i]
            i += 1
        
        i += 1 # skip over newline
        while line[i] != '\t' and line[i] != " ":
            inflected_form += line[i]
            i += 1
          
        inflected_form_to_base_form[inflected_form] = base_form

    return inflected_form_to_base_form

def main():
    return process_unimorph_file()

if __name__ == '__main__':
    main()