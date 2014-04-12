#
# Vagrantfile for Cabcom
# ======================
#
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  #config.vm.hostname = "cabcom.local"
  config.vm.box      = "ubuntu-1310-x64-virtualbox-puppet"
  config.vm.box_url  = "http://puppet-vagrant-boxes.puppetlabs.com/ubuntu-1310-x64-virtualbox-puppet.box"

  config.vm.provider "virtualbox" do |vbox|
    vbox.memory = 1024
  end

  # Forwarded port mapping for access to our project(s).
  config.vm.network :forwarded_port, guest: 8080, host: 8080

  # Enable provisioning with Puppet stand alone.
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path    = "puppet/manifests"
    puppet.manifest_file     = "site.pp"
    puppet.module_path       = "puppet/modules"
    puppet.facter = {
      "vagrant" => true
    }
  end
end

