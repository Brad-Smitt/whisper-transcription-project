export default function Home() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">iDoctor CR</h1>
      <p className="text-gray-700">Planifier les enregistrements audio/vidéo et générer des comptes rendus.</p>
      <div className="grid sm:grid-cols-2 gap-4">
        <a href="/agenda" className="border rounded p-4 hover:bg-gray-50">
          <div className="font-medium">Agenda</div>
          <div className="text-sm text-gray-600">Créer et gérer les rendez-vous</div>
        </a>
        <a href="/enregistrement" className="border rounded p-4 hover:bg-gray-50">
          <div className="font-medium">Enregistrement</div>
          <div className="text-sm text-gray-600">Capturer audio/vidéo, transcrire et résumer</div>
        </a>
      </div>
    </div>
  );
}
