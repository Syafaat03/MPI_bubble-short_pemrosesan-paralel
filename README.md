# BubbleSort-Pemrosesan-Paralel  
# Panduan Pembuatan Master dan Slave untuk Open MPI dengan Bubble Sort pada Ubuntu Desktop

Laporan ini memberikan langkah-langkah untuk membuat master dan slave, konfigurasi SSH, konfigurasi NFS, instalasi MPI, dan menjalankan kodingan Bubble Sort dengan Python pada Ubuntu Desktop.

## Daftar Isi
- [Device dan Tools yang Perlu Disiapkan](#device-dan-tools-yang-perlu-disiapkan)
- [Topologi Bridged](#topologi-bridged)
- [Pembuatan Master dan Slave](#pembuatan-master-dan-slave)
- [Konfigurasi SSH](#konfigurasi-ssh)
- [Konfigurasi NFS](#konfigurasi-nfs)
- [Instalasi MPI](#instalasi-mpi)
- [Running Code Python - Bubble Sort](#running-code-python---bubble-sort)

## Device dan Tools yang Perlu Disiapkan
1. Ubuntu Desktop
   - Ubuntu Desktop Master
   - Ubuntu Desktop Slave 1
   - Ubuntu Desktop Slave 2
   - Ubuntu Desktop Slave 3
2. MPI (Master dan Slave)
3. SSH (Master dan Slave)
4. NFS (Master dan Slave)
5. Code Bubble Sort Python

## Topologi Bridged
![Topologi Bubble sort](https://github.com/Syafaat03/laporan_bubble-short_pemrosesan-paralel/blob/12fea1576084fae2fbb3956af8d5367ee478cb93/Topologi%20Bubble%20Sort.png)


## Pembuatan Master dan Slave
1. Pastikan setiap master dan slave menggunakan Network Bridge Adapter dan terhubung ke internet.
2. Tentukan perangkat mana yang akan dijadikan master, slave1, slave2, dan slave3.
3. Buat user baru dengan perintah berikut pada master dan setiap slave:

    ```bash
    sudo adduser mpiuser
    ```

    Gantilah bagian 'master' menjadi 'slave1', 'slave2', dan seterusnya untuk slave.

4. Berikan akses kepada root dengan perintah:

    ```bash
    sudo usermod -aG sudo mpiuser
    ```

    Lakukan langkah di atas untuk setiap slave dengan mengganti pengguna 'master' menjadi 'slave1', 'slave2', dan seterusnya.

5. Masuk ke server dengan pengguna `mpiuser`:

    ```bash
    su - mpiuser
    ```

6. Update Ubuntu Desktop dan install tools:

    ```bash
    sudo apt update && sudo apt upgrade
    sudo apt install net-tools vim
    ```

7. Konfigurasi file `/etc/hosts` pada master, slave1, slave2, dan slave3. Daftarkan IP dan hostname masing-masing komputer.

## Konfigurasi SSH
1. Install OpenSSH pada master dan semua slave:

    ```bash
    sudo apt install openssh-server
    ```

2. Generate key pada master:

    ```bash
    ssh-keygen -t rsa
    ```

3. Copy key public ke setiap slave. Gunakan perintah berikut pada direktori `.ssh`:

    ```bash
    cd .ssh
    cat id_rsa.pub | ssh mpiuser@slave1 "mkdir .ssh; cat >> .ssh/authorized_keys"
    ```

    Ulangi perintah di atas untuk setiap slave.

## Konfigurasi NFS
1. Buat shared folder pada master dan setiap slave:

    ```bash
    mkdir bubble
    ```

2. Install NFS pada master:

    ```bash
    sudo apt install nfs-kernel-server
    ```

3. Konfigurasi file `/etc/export` pada master. Tambahkan baris berikut pada akhir file:

    ```plaintext
    /home/mpiuser/bubble *(rw,sync,no_root_squash,no_subtree_check)
    ```

    Lokasi Shared Folder adalah direktori tempat file bubble di atas dibuat.

4. Restart NFS Server:

    ```bash
    sudo exportfs -a
    sudo systemctl restart nfs-kernel-server
    ```

5. Install NFS pada setiap slave:

    ```bash
    sudo apt install nfs-common
    ```

6. Mount shared folder dari master ke setiap slave:

    ```bash
    sudo mount master:/home/mpiuser/bubble /home/mpiuser/bubble
    ```

    Ulangi perintah di atas untuk setiap slave.

## Instalasi MPI
1. Install Open MPI pada master dan semua slave:

    ```bash
    sudo apt install openmpi-bin libopenmpi-dev
    ```

2. Install library MPI melalui pip:

    ```bash
    sudo apt install python3-pip
    pip install mpi4py
    ```

## Running Code Python - Bubble Sort
1. Buatlah sebuah file python baru:

    ```bash
    touch /mpiuser/bubble/bubble.py
    ```

2. Masuk ke direktori tersebut dan edit file python:

    ```bash
    cd bubble
    nano bubble.py
    ```

    Lalu buatlah code Bubble Sort Python. Simpan dengan menekan `CTRL + X`.
   [bubble.py](https://github.com/Syafaat03/laporan_bubble-short_pemrosesan-paralel/blob/12fea1576084fae2fbb3956af8d5367ee478cb93/bubble.py)

3. Jalankan code tersebut pada master:

    ```bash
    mpirun -np 4 -host master,slave1,slave2,slave3 python3 bubble.py
    ```

   ![output](https://github.com/Syafaat03/laporan_bubble-short_pemrosesan-paralel/blob/12fea1576084fae2fbb3956af8d5367ee478cb93/output.png)
    Jika sudah keluar output seperti ini sudah berhasil, mengeluarkan output di semua master dan slave, outputnya menjadi 4 yaitu output dari master, slave1, slave2, slave3. Jadi yang kami urutkan disini berupa array: [5, 3, 4, 1, 2] diurutkan menjadi [1, 2, 3, 4, 5].

