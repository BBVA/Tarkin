VOCAB_RES_FOLDER=Tarkin/data/vocab
 
DEFAULT_DICT_URL=https://drive.google.com/uc?id=0B0ChLbwT19XcOVZFdm5wNXA5ODg
DEFAULT_DICT_NAME=SentiWordNet_3.0.0_20130122
 
function download_default_dict(){

    mkdir -p Tarkin/data/vocab

    # Download default lexicon file
    # SentiWordNet 3.0 by Stefano Baccianella, Andrea Esuli, and Fabrizio Sebastiani
    # http://sentiwordnet.isti.cnr.it

    curl -L $DEFAULT_DICT_URL -o $VOCAB_RES_FOLDER/$DEFAULT_DICT_NAME.tgz

    pushd $VOCAB_RES_FOLDER
    tar -xvf $DEFAULT_DICT_NAME.tgz --strip-components=5
    rm $DEFAULT_DICT_NAME.tgz
    popd

    check_file_existence $VOCAB_RES_FOLDER/$DEFAULT_DICT_NAME.txt

}

function check_file_existence(){
    if [ ! -f $1 ]; then
       echo "$0: The file '$1' does not exist, exiting..."
       exit 1
    fi
}

function check_folder_existence(){
    if [ ! -d $1 ]; then
       echo "$0: The directory '$1' does not exist, exiting..."
       exit 1
    fi
}

function create_temp_dir(){

    TMPDIRNAME=`mktemp -d "/tmp/tarkin-temp.XXXXXX"`
    if [ $? -ne 0 ]; then
       echo "$0: Can't create temp directory, exiting..."
       exit 1
    fi

    echo $TMPDIRNAME
}
